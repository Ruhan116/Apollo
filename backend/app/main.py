"""
Apollo Backend - FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import create_tables
from app.routers import auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    await create_tables()
    yield

app = FastAPI(
    title="Apollo API",
    description="AI-Powered Socratic Goal Mentor Platform",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# CORS Configuration
# TODO: Update origins for production deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Apollo API is running",
        "version": "1.0.0",
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "apollo-api"
    }


# TODO: Register routers when implemented
from app.routers import auth, goals
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(goals.router, prefix="/api/goals", tags=["Goals"])
# app.include_router(ai.router, prefix="/api/chat", tags=["AI Mentor"])
# app.include_router(community.router, prefix="/api/forums", tags=["Community"])
# app.include_router(notes.router, prefix="/api/notes", tags=["Notes"])
