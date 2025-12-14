# Apollo - AI-Powered Socratic Goal Mentor

**Competition**: Microsoft Imagine Cup 2025 - Education Theme
**Deadline**: December 28, 2025
**Team Size**: 3 members

## Project Overview

Apollo is an AI-powered goal achievement platform that acts as a Socratic mentor rather than a solution provider. The platform helps learners pursue self-chosen goals through:

- **Structured Planning**: Harada Method-based goal breakdown
- **Socratic AI Mentor**: Guides with questions instead of answers
- **Adaptive Scaffolding**: Dynamic micro-stepping when users are stuck
- **Peer Community**: Goal-based forums for support
- **Progress Tracking**: Streak-based habit formation

## Key Differentiators

- ✅ **Preserves Learning**: AI asks guiding questions, doesn't give direct answers
- ✅ **User-Chosen Goals**: No forced curriculum, pure self-direction
- ✅ **Emotional Support**: Dual AI system (Mentor + Emotional Support)
- ✅ **Adaptive Difficulty**: Dynamic micro-stepping based on genuine struggle detection
- ✅ **Community-Driven**: Peer matching and goal-based forums

## Tech Stack

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript 5.3+
- **Styling**: Tailwind CSS 3.4
- **UI Components**: Radix UI (accessible primitives)
- **State Management**: React Context API
- **Forms**: React Hook Form + Zod validation

### Backend
- **Framework**: FastAPI 0.110
- **Language**: Python 3.11+
- **Database**: PostgreSQL 15 (Azure or Supabase)
- **ORM**: SQLAlchemy 2.0 (async)
- **Migrations**: Alembic 1.13
- **Authentication**: JWT (python-jose)
- **AI**: Google Gemini 1.5 Flash

### Infrastructure
- **Architecture**: Monorepo (frontend + backend)
- **Hosting**: Azure App Service
- **Database**: Azure PostgreSQL / Supabase
- **Deployment**: Manual (Azure Portal) or GitHub Actions

## Repository Structure

```
apollo/
├── frontend/          # Next.js TypeScript application
│   ├── app/          # Next.js 14 App Router
│   ├── components/   # React components
│   ├── lib/          # Utilities and API client
│   └── README.md     # Frontend setup instructions
│
├── backend/          # FastAPI Python application
│   ├── app/          # Application code
│   │   ├── core/     # Config, database, security
│   │   ├── models/   # SQLAlchemy models
│   │   ├── routers/  # API endpoints
│   │   ├── services/ # Business logic
│   │   └── main.py   # Entry point
│   ├── alembic/      # Database migrations
│   ├── tests/        # Backend tests
│   └── README.md     # Backend setup instructions
│
└── docs/             # Project documentation
    ├── prd.md                    # Product Requirements
    ├── architecture.md           # Technical Architecture
    ├── brief.md                  # Project Brief
    └── 24-day-sprint-plan.md    # Development Timeline
```

## Quick Start

### Prerequisites

- **Node.js**: 18.17+ (for frontend)
- **Python**: 3.11+ (for backend)
- **PostgreSQL**: 15+ (local or cloud)
- **Git**: 2.40+

### 1. Clone Repository

```bash
git clone https://github.com/your-org/apollo.git
cd apollo
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start development server
uvicorn app.main:app --reload --port 8000
```

Backend will be running at: http://localhost:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with backend URL

# Start development server
npm run dev
```

Frontend will be running at: http://localhost:3000

### 4. Verify Setup

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

## Development Workflow

### Code Quality

**Backend:**
```bash
cd backend
black app/ tests/          # Format code
ruff check app/ tests/     # Lint code
mypy app/                  # Type checking
pytest                     # Run tests
```

**Frontend:**
```bash
cd frontend
npm run lint              # ESLint
npm run format            # Prettier (if configured)
npm test                  # Run tests
```

### Database Migrations

Create migration after model changes:
```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

### Running Both Services

**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## Project Documentation

Comprehensive documentation is available in the [docs/](docs/) directory:

- **[PRD](docs/prd.md)**: Product Requirements Document with features, user stories, and success metrics
- **[Architecture](docs/architecture.md)**: Technical architecture, database schema, API design
- **[Brief](docs/brief.md)**: Project overview, problem statement, target users
- **[Sprint Plan](docs/24-day-sprint-plan.md)**: 24-day development timeline for competition

## MVP Feature Roadmap

### Epic 1: Foundation & Authentication ✅
- Monorepo setup
- User registration/login (JWT)
- Azure deployment pipeline

### Epic 2: AI-Powered Goal Planning 🚧
- Goal input with natural language
- Gemini-powered Harada plan generation
- Goal editing and management

### Epic 3: Socratic Mentor & Progress Tracking 📋
- Dual AI system (Mentor + Emotional Support)
- Chat interface with context switching
- Streak tracking and daily check-ins

### Epic 4: Dynamic Micro-Stepping (P1 - Optional) 📋
- Stuck detection algorithm
- Adaptive scaffolding with micro-steps

### Epic 5: Community & Notes (P1 - Optional) 📋
- Goal-based forums
- Personal note-taking

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/apollo
JWT_SECRET_KEY=your-secret-key
GEMINI_API_KEY=your-gemini-key
ENVIRONMENT=development
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

See `.env.example` files in each directory for complete configuration.

## Deployment

### Azure App Service (Production)

**Backend:**
1. Create Azure App Service (Python 3.11 runtime)
2. Configure environment variables in Azure Portal
3. Deploy via Git or Azure CLI
4. Run migrations: `alembic upgrade head`

**Frontend:**
1. Create Azure Static Web App or App Service (Node runtime)
2. Configure build settings (Next.js)
3. Deploy via Git or Azure CLI

See [docs/deployment-guide.md](docs/deployment-guide.md) for detailed instructions (TODO).

## Testing Strategy

- **Unit Tests**: Core business logic (goal creation, progress calculation, streak tracking)
- **Integration Tests**: API endpoints, database operations
- **Manual Testing**: UI/UX flows, AI conversation quality
- **No E2E Automation**: Manual QA checklist for MVP

**Coverage Goals**: 60%+ on services/repositories

## Competition Timeline

- **Deadline**: December 28, 2025
- **Development**: 18-20 days
- **Beta Testing**: 3-4 days
- **Submission**: December 28, 2025

**Current Sprint**: Epic 1 - Foundation & Authentication

## Contributing

This is a competition project with tight deadlines. Team members should:

1. Follow coding standards (see backend/pyproject.toml, frontend/.eslintrc)
2. Write tests for core logic
3. Use meaningful commit messages
4. Keep PRs focused and small
5. Review PRs promptly

## Team

- **Team Member 1**: [Role]
- **Team Member 2**: [Role]
- **Team Member 3**: [Role]

## License

MIT License - Microsoft Imagine Cup 2025 Project

---

**Built for Microsoft Imagine Cup 2025 - Education Theme**
*"AI is reshaping the way institutions support learners and teachers alike"*
