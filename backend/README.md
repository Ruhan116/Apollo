# Apollo Backend

FastAPI backend for Apollo - AI-Powered Socratic Goal Mentor Platform.

## Tech Stack

- **Framework**: FastAPI 0.110.0
- **Language**: Python 3.11+
- **Database**: PostgreSQL with SQLAlchemy 2.0 (async)
- **AI**: Google Gemini 1.5 Flash
- **Authentication**: JWT with python-jose
- **Migrations**: Alembic

## Project Structure

```
backend/
├── app/
│   ├── core/           # Configuration, database, security
│   ├── models/         # SQLAlchemy ORM models
│   ├── schemas/        # Pydantic request/response schemas
│   ├── repositories/   # Repository pattern for data access
│   ├── services/       # Business logic layer
│   ├── prompts/        # Gemini AI system prompts
│   ├── routers/        # FastAPI route handlers
│   ├── dependencies.py # FastAPI dependencies
│   └── main.py         # Application entry point
├── alembic/            # Database migrations
├── tests/              # Backend tests
└── requirements.txt    # Python dependencies
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
- Database connection string
- JWT secret key
- Gemini API key
- Other settings

### 4. Database Setup

**Option A: Local PostgreSQL**
```bash
# Install PostgreSQL locally
# Create database: apollo
# Update DATABASE_URL in .env
```

**Option B: Supabase (Recommended for Development)**
1. Create free account at https://supabase.com
2. Create new project
3. Copy connection string to `.env`

**Run Migrations:**
```bash
alembic upgrade head
```

### 5. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- **API Root**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Development

### Code Quality

Format code:
```bash
black app/ tests/
```

Lint code:
```bash
ruff check app/ tests/
```

Type checking:
```bash
mypy app/
```

### Testing

Run tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app --cov-report=html
```

### Database Migrations

Create new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback migration:
```bash
alembic downgrade -1
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

## Architecture

### Modular Monolith
- Single deployable application
- Clear module boundaries via routers
- Repository pattern for data access
- Service layer for business logic

### Key Modules
- **Auth**: User registration, login, JWT tokens
- **Goals**: Goal creation, action steps, progress
- **AI**: Gemini integration, Socratic mentor, emotional support
- **Community**: Forums, posts, replies (Epic 5)
- **Notes**: Personal note-taking (Epic 5)

## Environment Variables

See `.env.example` for complete list. Key variables:

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret for signing JWT tokens
- `GEMINI_API_KEY`: Google Gemini API key
- `ENVIRONMENT`: development/production
- `CORS_ORIGINS`: Allowed frontend origins

## Deployment

### Azure App Service (Production)

1. Create Azure App Service (Python 3.11 runtime)
2. Set environment variables in Azure portal
3. Deploy via Git or Azure CLI
4. Run migrations: `alembic upgrade head`

See main README.md for detailed deployment instructions.

## License

MIT License - Microsoft Imagine Cup 2025 Project
