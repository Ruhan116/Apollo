"""Authentication service"""
from app.schemas.auth import UserCreate, UserLogin
from sqlalchemy.ext.asyncio import AsyncSession
from email_validator import validate_email, EmailNotValidError
from password_validator import PasswordValidator
from app.repositories.user import UserRepository
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from typing import Optional
from app.config import settings

# Password hashing context — prefer Argon2, keep bcrypt for legacy verification
pwd_context = CryptContext(schemes=["argon2", "bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.user_repo = UserRepository(db)
        self.db = db

    def _hash_password(self, password: str) -> str:
        try:
            # Explicitly use Argon2 for new hashes
            return pwd_context.hash(password, scheme="argon2")
        except ValueError as e:
            # Convert any low-level hash errors to HTTP 400
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def _create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        return encoded_jwt

    async def register_user(self, user_data: UserCreate) -> dict:
        """Register a new user"""
        # Validate email
        try:
            valid_email = validate_email(user_data.email)
            user_data.email = valid_email.email
        except EmailNotValidError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid email: {str(e)}"
            )

        # Validate password
        schema = PasswordValidator()
        schema.min(8).max(100).has().uppercase().has().lowercase().has().digits()

        if not schema.validate(user_data.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be 8-100 characters with uppercase, lowercase, and digits"
            )

        # Check if user already exists
        existing_user = await self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Hash password
        hashed_password = self._hash_password(user_data.password)
        user_data.password = hashed_password

        # Create user record
        created_user = await self.user_repo.create(user_data)

        # Create access token
        access_token_expires = timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS)
        access_token = self._create_access_token(
            data={"sub": created_user.email, "user_id": created_user.id},
            expires_delta=access_token_expires
        )

        return {
            "user": {
                "id": created_user.id,
                "email": created_user.email,
                "created_at": created_user.created_at
            },
            "access_token": access_token,
            "token_type": "bearer"
        }

    async def login(self, user_data: UserLogin) -> dict:
        """Authenticate user and return JWT token"""
        user = await self.user_repo.get_by_email(user_data.email)

        if not user or not self._verify_password(user_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # If the stored password uses a legacy scheme (e.g., bcrypt), rehash with Argon2 transparently
        try:
            if pwd_context.needs_update(user.hashed_password):
                new_hash = self._hash_password(user_data.password)
                await self.user_repo.update_password(user, new_hash)
        except Exception:
            # Non-fatal: continue authentication even if rehashing/updating fails
            pass

        # Create access token
        access_token_expires = timedelta(hours=settings.JWT_ACCESS_TOKEN_EXPIRE_HOURS)
        access_token = self._create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email
            }
        }

    async def verify_token(self, token: str) -> dict:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
            email: str = payload.get("sub")
            user_id: int = payload.get("user_id")

            if email is None or user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials"
                )

            return {"email": email, "user_id": user_id}
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

    async def get_user_by_id(self, user_id: int) -> dict:
        """Get user by ID (for other services)"""
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return {
            "id": user.id,
            "user_name": user.user_name,
            "email": user.email,
            "created_at": user.created_at
        }
