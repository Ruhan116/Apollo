# Epic 1: Foundation & Authentication

**Project:** Apollo
**Epic Goal:** Establish project infrastructure, Azure deployment pipeline, database schema, and user authentication system. Deliver a working landing page with signup/login functionality, proving the technical stack is operational and the team can deploy to production. This creates the foundation for all feature development while delivering a minimal but complete vertical slice (user can register, log in, and see a dashboard).

**Priority:** P0 (Must Have)
**Estimated Timeline:** Days 1-5 of development
**Dependencies:** None (foundational epic)

---

## Story 1.1: Initialize Monorepo and Development Environment

**As a** developer,
**I want** a fully configured monorepo with Next.js frontend (TypeScript) and FastAPI backend (Python),
**so that** the team can start building features with consistent tooling and clear separation of concerns.

### Acceptance Criteria

1. Monorepo structure created with `/frontend` (Next.js + TypeScript) and `/backend` (FastAPI + Python)
2. Frontend: TypeScript configured with strict mode, Next.js 14+ App Router initialized
3. Backend: Python 3.11+ virtual environment, FastAPI project structure with main.py, requirements.txt
4. Code quality tools configured:
   - Frontend: ESLint + Prettier
   - Backend: Black + Ruff + mypy, pyproject.toml for tool configuration
5. Pre-commit hooks configured using pre-commit framework for both frontend and backend
6. Development scripts work: frontend (`npm run dev`), backend (`uvicorn app.main:app --reload`)
7. Environment variable management: `.env.example` files in both frontend and backend with required variables documented
8. Git repository initialized with `.gitignore` excluding `node_modules`, `.venv`, `__pycache__`, `.env`
9. README.md documents monorepo structure, setup instructions for both frontend and backend, and how to run locally

### Technical Notes

- **Frontend Tech Stack:** Next.js 14+, TypeScript 5.3.3, React 18.3.0, Tailwind CSS 3.4.0
- **Backend Tech Stack:** Python 3.11+, FastAPI 0.110.0, Uvicorn 0.28.0
- **Code Quality:** ESLint 8.57.0, Prettier 3.2.0, Black 24.2.0, Ruff 0.3.0, mypy 1.9.0
- **Version Control:** Git 2.40+, GitHub repository

### Definition of Done

- [ ] Both frontend and backend start successfully in development mode
- [ ] All linters and formatters run without errors
- [ ] Pre-commit hooks execute on git commit
- [ ] README.md contains complete setup instructions
- [ ] All team members can clone repo and run locally

---

## Story 1.2: Set Up Azure Infrastructure and Database

**As a** developer,
**I want** Azure App Service and PostgreSQL database provisioned and accessible,
**so that** the application can be deployed to production and persist user data.

### Acceptance Criteria

1. Azure App Service created (Free or Basic tier) for hosting the FastAPI (Python) backend API
2. Azure Database for PostgreSQL (Basic tier) provisioned with connection string stored in Azure App Service environment variables
3. Database connection verified from local development using connection string (can connect and run basic query)
4. SQLAlchemy installed and configured with Base model class and initial `User` model with fields: id, email, password_hash, created_at, updated_at
5. Alembic initialized for database migrations, initial migration created defining User table
6. Migration successfully applied to Azure PostgreSQL database (`alembic upgrade head`)
7. Database connection pooling configured using SQLAlchemy async engine
8. Azure App Service can connect to database (verified via `/health` endpoint returning database status)

### Technical Notes

- **Database:** PostgreSQL 15.0 (Azure Database for PostgreSQL or Supabase)
- **ORM:** SQLAlchemy 2.0.28 with async support
- **Migrations:** Alembic 1.13.0
- **Connection Pooling:** Async SQLAlchemy engine with connection pool settings
- **Health Check:** Simple `/health` endpoint that queries database and returns status

### Database Schema (User Model)

```python
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(60), nullable=False)  # bcrypt hash length
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

### Definition of Done

- [ ] Azure App Service and PostgreSQL provisioned and accessible
- [ ] Database connection works from local development environment
- [ ] SQLAlchemy models defined and Alembic migrations applied
- [ ] `/health` endpoint returns successful database connection status
- [ ] Environment variables documented in `.env.example`

---

## Story 1.3: Implement User Registration and Authentication

**As a** new user,
**I want** to create an account with email and password and log in securely,
**so that** my goals and progress are saved to my personal account.

### Acceptance Criteria

1. `/api/auth/register` POST endpoint accepts email and password, validates input (email format, password min 8 chars), hashes password with bcrypt, creates User record in database, returns success response
2. `/api/auth/login` POST endpoint accepts email and password, verifies credentials against database, generates JWT access token (24-hour expiry), returns token in response
3. JWT token includes user ID and email in payload, signed with secret from environment variable
4. `/api/auth/me` GET endpoint requires valid JWT in Authorization header, returns current user's profile (id, email) or 401 Unauthorized if token invalid/missing
5. Password validation prevents common weak passwords (e.g., "password123") using simple rules (min 8 chars, at least 1 number)
6. Duplicate email registration returns 400 error with message "Email already registered"
7. Login with incorrect password returns 401 error without revealing whether email exists (security best practice)

### Technical Notes

- **Authentication Library:** python-jose 3.3.0 for JWT generation/validation
- **Password Hashing:** passlib 1.7.4 with bcrypt algorithm
- **Token Expiry:** 24 hours for MVP (configurable via environment variable)
- **Security:** JWT signed with HS256 algorithm, secret from `JWT_SECRET` env var

### API Endpoints

**POST /api/auth/register**
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response (201 Created):
{
  "id": "uuid-here",
  "email": "user@example.com",
  "created_at": "2025-12-14T10:00:00Z"
}
```

**POST /api/auth/login**
```json
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123"
}

Response (200 OK):
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "user": {
    "id": "uuid-here",
    "email": "user@example.com"
  }
}
```

**GET /api/auth/me**
```
Headers: Authorization: Bearer {token}

Response (200 OK):
{
  "id": "uuid-here",
  "email": "user@example.com"
}
```

### Definition of Done

- [ ] Registration endpoint creates users with hashed passwords
- [ ] Login endpoint returns valid JWT tokens
- [ ] JWT tokens are validated correctly on protected endpoints
- [ ] Password validation prevents weak passwords
- [ ] Security best practices followed (no user enumeration, proper error messages)
- [ ] All endpoints tested with valid and invalid inputs

---

## Story 1.4: Build Frontend Authentication UI

**As a** new user,
**I want** a signup and login page with clear forms and error messages,
**so that** I can easily create an account and access the application.

### Acceptance Criteria

1. `/signup` page displays form with email input, password input, and "Create Account" button using React Hook Form + Zod validation
2. Signup form validates email format and password requirements (min 8 chars) client-side before submission
3. Successful signup redirects to `/dashboard` and stores JWT token in localStorage (or httpOnly cookie if time permits)
4. Signup errors (duplicate email, validation failures) display as inline error messages below form inputs
5. `/login` page displays form with email input, password input, and "Log In" button
6. Successful login redirects to `/dashboard` and stores JWT token
7. Login errors (incorrect credentials) display generic "Invalid email or password" message (no user enumeration)
8. Both pages include link to switch between signup/login ("Already have an account? Log in" and vice versa)
9. Pages use Tailwind CSS for styling with responsive mobile layout

### Technical Notes

- **Form Library:** React Hook Form 7.51.0
- **Validation:** Zod 3.22.0 for type-safe schema validation
- **Styling:** Tailwind CSS 3.4.0 with responsive utilities
- **State Management:** React Context API for auth state
- **Token Storage:** localStorage (consider httpOnly cookies for enhanced security post-MVP)

### UI Components Needed

- Email input field (type="email")
- Password input field (type="password", min 8 chars validation)
- Submit button (disabled during API call, shows loading state)
- Error message display (inline below inputs)
- Navigation links (switch between signup/login)

### Form Validation Rules

```typescript
const signupSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[0-9]/, "Password must contain at least one number")
});
```

### Definition of Done

- [ ] Signup page functional with form validation
- [ ] Login page functional with form validation
- [ ] Forms display appropriate error messages
- [ ] Successful auth redirects to dashboard
- [ ] JWT tokens stored and retrieved correctly
- [ ] Responsive design works on mobile and desktop
- [ ] Links to switch between signup/login work

---

## Story 1.5: Create Protected Dashboard and Deploy to Azure

**As a** logged-in user,
**I want** to see a personalized dashboard after login,
**so that** I know authentication worked and I'm in the application.

### Acceptance Criteria

1. `/dashboard` page is protected route that checks for valid JWT token on mount, redirects to `/login` if token missing or expired
2. Dashboard displays "Welcome, [user email]!" message and placeholder content ("Your goals will appear here soon")
3. Dashboard includes "Log Out" button that clears JWT token and redirects to `/login`
4. Frontend makes authenticated API call to `/api/auth/me` to verify token validity and fetch user profile
5. Application deployed to Azure App Service with both frontend and backend accessible via public URL
6. Environment variables configured in Azure App Service (database connection, JWT secret)
7. Deployment pipeline allows team to push updates (manual deploy via Azure portal or Git deployment acceptable for MVP)
8. Public URL loads landing page with "Sign Up" and "Log In" buttons that navigate to respective pages
9. End-to-end flow works in production: User can sign up → log in → see dashboard → log out

### Technical Notes

- **Protected Routes:** Next.js middleware or React Context to check auth status
- **API Client:** Typed fetch wrappers in `lib/api.ts` with auth headers
- **Deployment:** Azure App Service for both frontend (Next.js) and backend (FastAPI)
- **Environment Variables:** Configure in Azure portal under Configuration settings

### Deployment Checklist

- [ ] Backend deployed to Azure App Service (Python runtime)
- [ ] Frontend deployed to Azure Static Web Apps or same App Service
- [ ] Environment variables configured (DATABASE_URL, JWT_SECRET, GEMINI_API_KEY placeholder)
- [ ] Public URL accessible
- [ ] HTTPS enabled (automatic with Azure)
- [ ] Database migrations applied to production database

### Dashboard UI Elements

- Welcome message with user email
- Placeholder for goals list (empty state)
- Placeholder for streak counter (to be implemented in Epic 3)
- "Log Out" button
- Navigation header (to be expanded in future epics)

### Definition of Done

- [ ] Dashboard shows personalized welcome message
- [ ] Protected route redirects unauthenticated users to login
- [ ] Log out button clears token and redirects
- [ ] Application deployed to Azure and accessible via public URL
- [ ] End-to-end auth flow works in production
- [ ] Environment variables properly configured
- [ ] Team can deploy updates successfully

---

## Epic 1 Summary

### Stories Completed
- 5 stories total
- All P0 (must-have) stories

### Key Deliverables
1. ✅ Monorepo with Next.js frontend and FastAPI backend
2. ✅ Azure infrastructure (App Service + PostgreSQL)
3. ✅ User authentication system (registration, login, JWT)
4. ✅ Frontend auth UI (signup, login, dashboard)
5. ✅ Production deployment to Azure

### Technical Foundation Established
- Monorepo structure with clear separation of concerns
- Code quality tools (linters, formatters, type checking)
- Database with migrations (SQLAlchemy + Alembic)
- Secure authentication (JWT with bcrypt password hashing)
- Deployment pipeline to Azure
- Health monitoring (`/health` endpoint)

### What's Next
With Epic 1 complete, the team has a solid foundation to build features. Epic 2 will implement the core value proposition: AI-powered goal planning with Gemini integration.

**Ready for Epic 2: AI-Powered Goal Planning** 🚀
