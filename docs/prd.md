# Apollo Product Requirements Document (PRD)

**Project Name:** Apollo
**Date:** 2025-12-14
**PRD Version:** 1.0
**Competition:** Microsoft Imagine Cup 2025 - Education Theme
**Deadline:** December 28, 2025 (24 days)

---

## Goals and Background Context

### Goals

- Enable learners to achieve self-chosen goals through AI-powered Socratic mentorship that preserves the learning process
- Match learners with peers and mentors working on similar goals to provide community support and reduce isolation
- Deliver adaptive scaffolding that removes unproductive friction while maintaining productive struggle
- Achieve top 10 finish in Microsoft Imagine Cup regional rounds by demonstrating superior learning outcomes vs. existing AI tools
- Validate that Socratic AI guidance combined with peer support leads to higher goal completion rates (25%+ within 60 days) than solo AI tool usage
- Build a platform where speed and learning are both maximized by redirecting AI capabilities to guidance rather than solution provision

### Background Context

Current AI education tools create a critical paradox: they either provide instant answers that eliminate learning (ChatGPT, Claude) or assign curriculum without support that leads to disengagement (traditional education, MOOCs with 70-90% dropout rates). Students develop dependency on AI-generated solutions without understanding, losing metacognitive skills and problem-solving ability. Simultaneously, productive struggle that builds skills is confused with unproductive friction (unclear steps, missing resources, isolation) that causes goal abandonment.

Apollo addresses this crisis by combining the Harada Method's structured goal planning with a dual AI system (Socratic Mentor AI that asks questions rather than providing answers, and Emotional Support AI that detects frustration and provides encouragement), peer community infrastructure organized by goal type, and dynamic micro-stepping that breaks overwhelming tasks into 5-10 minute actions while preserving user agency. The platform targets self-directed learners (ages 16-35) who use existing AI tools but recognize they aren't retaining knowledge, serving a market ready for "AI that makes you smarter" rather than "AI that makes you lazy."

### Change Log

| Date | Version | Description | Author |
|------|---------|-------------|--------|
| 2025-12-14 | 1.0 | Initial PRD creation from Project Brief | John (PM) |

---

## Requirements

### Functional Requirements

1. **FR1:** The system shall allow users to input a goal description in natural language and generate a personalized Harada-style plan with flexible numbers of sub-goals and action steps
2. **FR2:** The system shall provide a Mentor AI that uses Socratic questioning methodology and refuses to provide direct answers to user questions
3. **FR3:** The system shall provide an Emotional Support AI that detects user frustration patterns and provides encouragement and context-switching suggestions
4. **FR4:** The system shall intelligently switch between Mentor AI and Emotional Support AI based on progress history and emotion analysis
5. **FR5:** The system shall allow users to request modifications to their generated plan (e.g., "this step is unreachable")
6. **FR6:** The system shall track daily user activity and maintain a streak counter showing consecutive days of engagement
7. **FR7:** The system shall prompt users with daily check-ins asking "What are you working on today?"
8. **FR8:** The system shall provide visual progress indicators for goals and action steps showing completion percentage
9. **FR9:** The system shall detect when a user is genuinely stuck (not lazy) using progress history and emotion analysis
10. **FR10:** The system shall dynamically break down action steps into 5-10 minute micro-steps when users are genuinely stuck
11. **FR11:** The system shall allow users to exit micro-stepping scaffolding when ready to return to normal action steps
12. **FR12:** The system shall provide goal-type based community forums that are auto-created as users join with matching goals
13. **FR13:** The system shall allow users to post questions, share progress updates, and provide peer support in forums
14. **FR14:** The system shall provide upvote and reply functionality for forum posts
15. **FR15:** The system shall allow users to capture notes, insights, resources, and reflections per goal with basic markdown support
16. **FR16:** The system shall require user authentication with email-based signup/login
17. **FR17:** The system shall associate all goals, progress, notes, and forum activity with authenticated user accounts
18. **FR18:** The system shall provide a user dashboard showing active goals, current streaks, and recent forum activity

### Non-Functional Requirements

1. **NFR1:** AI Mentor responses must be delivered within 3 seconds of user input under normal load conditions
2. **NFR2:** Page load time must be under 2 seconds for initial load and under 1 second for subsequent navigation
3. **NFR3:** Forum posts must appear to all users within 5 seconds of submission
4. **NFR4:** The system must support modern browsers (Chrome, Firefox, Safari, Edge - last 2 versions only)
5. **NFR5:** The system must provide mobile-responsive design working on iOS Safari and Android Chrome
6. **NFR6:** The platform must be accessible as a Progressive Web App (PWA) with offline viewing capability for notes and progress (P1 - nice-to-have)
7. **NFR7:** Hosting costs must target $0/month using Azure free credits and Gemini free tier
8. **NFR8:** LLM API calls must implement strict rate limiting per user to prevent exceeding Gemini free tier quota (1500 requests/day)
9. **NFR9:** The Mentor AI must successfully use Socratic questioning (not direct answers) in 75%+ of interactions as measured by manual review
10. **NFR10:** Emotion detection accuracy must achieve 75%+ user confirmation rate when "stuck" is detected
11. **NFR11:** The system must encrypt user data at rest and in transit
12. **NFR12:** The system must implement basic content moderation including profanity filtering for forum posts
13. **NFR13:** The system must comply with GDPR requirements for EU users including data export and deletion capabilities
14. **NFR14:** The system must be deployable and functional by December 28, 2025 (24-day development timeline)
15. **NFR15:** The codebase must use TypeScript for frontend and Python with type hints (Pydantic) for backend type safety
16. **NFR16:** The system must support English language only for MVP release

---

## User Interface Design Goals

### Overall UX Vision

Apollo should feel like a **personal growth companion** rather than a productivity tool or classroom. The interface prioritizes **calm focus and encouragement** over urgency and notifications. Visual design should convey **trust, warmth, and progress** - users need to feel safe to struggle and safe to ask "dumb questions." The experience should be **conversational and human**, with the AI mentor feeling like a patient guide, not a robotic chatbot. Every interaction should reinforce the core message: "We're here to help you grow, not to do the work for you."

Key UX principles:
- **Clarity over cleverness** - No hidden features, clear CTAs, obvious next steps
- **Progress visibility** - Users always know where they are in their journey
- **Low cognitive load** - One primary action per screen, minimal distractions
- **Encouragement over pressure** - Streaks celebrate consistency, not shame missed days
- **Human-centered AI** - Chat interface feels natural, not transactional

### Key Interaction Paradigms

1. **Conversational Goal Setup** - Users describe goals in their own words (text input), AI responds conversationally to refine and structure the plan
2. **Daily Check-In Ritual** - Each session starts with "What are you working on today?" to establish focus and continuity
3. **Chat-First AI Mentor** - Primary interaction is persistent chat thread with Mentor AI, organized by goal/action step context
4. **Micro-Step Progressive Disclosure** - When scaffolding is triggered, micro-steps appear inline as expandable/collapsible guidance, not a separate mode
5. **Ambient Progress Indicators** - Streaks, completion percentages, and visual progress always visible but not intrusive
6. **Forum as Discovery, Not Obligation** - Community is accessible but optional; users can opt into social features at their own pace
7. **Note-Taking as Reflection** - Integrated markdown editor appears contextually when users complete steps or have insights to capture

**Assumption:** Given 24-day timeline, we're assuming **web-first, single-column mobile layout** (no complex responsive breakpoints) with **minimal animation/transitions** to accelerate development.

### Core Screens and Views

From a product perspective, these are the critical screens necessary to deliver the PRD values and goals:

1. **Onboarding/Goal Input Screen** - Where users first describe their goal and see AI-generated plan
2. **Dashboard (Home)** - Shows active goals, current streak, today's focus, recent forum activity
3. **Goal Detail View** - Displays full goal structure (sub-goals, action steps), progress visualization, AI chat thread
4. **AI Mentor Chat Interface** - Full-screen conversational interface with Mentor AI or Emotional Support AI
5. **Micro-Stepping View** - Inline breakdown of current action step into 5-10 min tasks (appears within Goal Detail)
6. **Community Forums Home** - Browse goal-type forums, see trending posts, search
7. **Forum Thread View** - Read posts, replies, upvote, add comments
8. **Notes/Reflection Editor** - Per-goal markdown note-taking space
9. **Profile/Settings** - User preferences, notification settings, data export/deletion (GDPR)

**Assumption:** Authentication screens (login/signup) are assumed standard and not listed as "core product screens."

### Accessibility: WCAG AA

Target WCAG 2.1 Level AA compliance for MVP:
- Keyboard navigation for all interactive elements
- Sufficient color contrast (4.5:1 for text, 3:1 for UI components)
- Screen reader support with proper ARIA labels
- Responsive text sizing (supports browser zoom up to 200%)
- Focus indicators visible on all interactive elements

**Rationale:** WCAG AA is industry standard and achievable within timeline. AAA would require significant additional effort (e.g., 7:1 contrast, sign language) that conflicts with 24-day constraint. Education platform should be accessible to users with disabilities.

**Assumption:** No custom accessibility features beyond WCAG AA (e.g., dyslexia-friendly fonts, high-contrast themes) for MVP.

### Branding

**Visual Identity:**
- **Tone:** Warm, encouraging, human (not corporate or sterile)
- **Color Palette:** Calming, growth-oriented colors - suggest blues/greens for trust and growth, warm accent colors for encouragement (specific hex values TBD by design phase)
- **Typography:** Highly readable sans-serif for UI, optionally a warmer font for AI mentor messages to feel conversational
- **Imagery:** Minimal, focus on iconography for goal types, progress indicators, and micro-interactions

**Voice & Tone:**
- **Mentor AI:** Patient, inquisitive, non-judgmental - "What makes you think that approach would work?" vs. "That's wrong"
- **Emotional Support AI:** Warm, empathetic, validating - "It sounds like you're feeling stuck. That's completely normal - let's break this down together"
- **UI Copy:** Direct, encouraging, action-oriented - "Start your first goal" vs. "Click here to begin the goal creation process"

**Assumption:** No existing brand guidelines or logo. Team will create simple, clean branding during development. Focus on **functional design over visual polish** given timeline.

### Target Device and Platforms: Web Responsive

**Primary Platform:** Web application (desktop and mobile browsers)
- Desktop: 1280px+ wide screens (laptop/desktop primary use case for focused learning sessions)
- Tablet: 768px-1279px (iPad landscape/portrait)
- Mobile: 320px-767px (smartphones - critical for daily check-ins and streak maintenance)

**Progressive Web App (PWA):**
- Installable on mobile devices for app-like experience
- Offline capability for viewing notes and progress (no AI interaction offline)
- Push notifications for streak reminders (if user opts in)

**Browser Support:**
- Chrome/Edge (Chromium) - last 2 versions
- Firefox - last 2 versions
- Safari (iOS and macOS) - last 2 versions
- **No support for:** IE11, legacy mobile browsers, Opera Mini

**Assumption:** No native iOS/Android apps for MVP. PWA provides sufficient mobile experience without App Store complexity.

---

## Technical Assumptions

### Repository Structure: Monorepo

**Decision:** Use a **monorepo structure** for managing frontend and backend codebases in a single repository.

**Rationale:**
- Simplified dependency management and versioning for small team (3 people)
- Single version control and deployment strategy reduces complexity for 24-day timeline
- Easier to coordinate changes across frontend and backend
- Shared documentation and API specifications in one place

**Structure:**
```
/frontend      (Next.js app - TypeScript)
/backend       (FastAPI app - Python)
/docs          (Shared documentation, API specs)
/.github       (CI/CD workflows)
```

### Service Architecture

**Decision:** **Modular monolith** - Single deployable backend application with clear internal module boundaries (auth, goals, ai-mentor, forums, notes).

**Rationale:**
- **Speed to delivery:** No microservices overhead (service discovery, inter-service communication, distributed tracing)
- **Cost efficiency:** Single Azure App Service instance vs. multiple services (critical for <$100/month constraint)
- **Simpler debugging:** All code runs in one process during development and production
- **Future-proofing:** Modular structure allows extracting services later if specific modules need independent scaling
- **Team size:** 3 developers don't need microservices complexity

**Module Boundaries (FastAPI Routers):**
- `routers/auth.py`: User authentication, session management (JWT tokens)
- `routers/goals.py`: Goal creation, action steps, progress tracking
- `routers/ai.py`: LLM API integration, Mentor AI, Emotional Support AI, prompt management
- `routers/community.py`: Forums, posts, replies, upvotes
- `routers/notes.py`: Note-taking, markdown storage

**NOT using:**
- Microservices (too complex for timeline/team size)
- Serverless-only architecture (cold starts would violate 3s AI response NFR)
- Edge functions for everything (debugging complexity, vendor lock-in)

### Testing Requirements

**Decision:** **Unit tests + critical integration tests only** - Pragmatic testing for 24-day timeline.

**Testing Strategy:**
- **Unit tests:** Core business logic (goal creation, progress calculation, streak tracking) and AI prompt construction
- **Integration tests:** Critical API endpoints (auth flow, goal CRUD, AI chat) and database operations
- **Manual testing:** UI/UX flows, AI conversation quality, forum interactions
- **NO E2E automation for MVP:** Playwright/Cypress would consume too much time; rely on manual QA before competition submission

**Rationale:**
- **Timeline constraints:** E2E test infrastructure takes days to set up properly
- **AI testing complexity:** Mentor AI quality requires human judgment (Socratic questioning), not automated assertions
- **Focus on core logic:** Ensure business rules work correctly (streaks, progress, micro-stepping triggers)
- **Manual validation for demo:** Competition judges see live demo, so manual QA more valuable than test coverage percentage

**Testing Tools:**
- **Frontend:** Jest + React Testing Library for component tests
- **Backend:** pytest for unit/integration tests, FastAPI TestClient for API endpoint testing
- Manual testing checklist for UI flows (part of PM checklist before submission)

### Additional Technical Assumptions and Requests

**Frontend Stack:**
- **Framework:** Next.js 14+ (App Router) for React with SSR/SSG benefits and file-based routing
- **Styling:** Tailwind CSS for rapid UI development with utility-first approach
- **State Management:** React Context API for global state (user auth, current goal) - avoid Redux complexity for MVP
- **UI Components:** Headless UI or Radix UI for accessible primitives (modals, dropdowns) to accelerate WCAG AA compliance
- **Markdown Rendering:** react-markdown for note display
- **Form Handling:** React Hook Form with Zod validation for type-safe forms

**Backend Stack:**
- **Runtime:** Python 3.11+ (async/await support for concurrent requests)
- **Framework:** FastAPI (modern, fast, auto-generates OpenAPI docs, excellent async support)
- **API Style:** RESTful API with automatic OpenAPI/Swagger documentation
- **WebSockets:** FastAPI WebSocket support for real-time forum updates (5-second NFR requirement) - OPTIONAL, may use polling if setup >4 hours
- **Authentication:** JWT tokens using python-jose library OR Azure AD B2C integration
- **Session Management:** JWT access tokens (short-lived) with refresh tokens
- **Type Safety:** Pydantic models for request/response validation and serialization

**Database & Storage:**
- **Primary Database:** PostgreSQL (Azure Database for PostgreSQL or Supabase hosted)
  - Relational data: users, goals, action_steps, forum_posts, notes
  - JSONB columns for flexible goal structures if needed (Harada plan variations)
- **ORM:** SQLAlchemy 2.0+ with async support OR Tortoise ORM for type-safe database access
- **Migrations:** Alembic for database schema migrations
- **Caching:** Redis (Azure Cache for Redis or Upstash) OR in-memory caching to avoid extra service
- **File Storage:** Azure Blob Storage if user-uploaded resources needed (likely not MVP)

**AI/LLM Integration:**
- **Primary LLM:** Google Gemini 1.5 Flash (free tier: 15 RPM, 1M TPM, 1500 RPD)
- **Cost:** $0 for competition timeline (no API costs!)
- **Fallback Model:** Gemini 1.5 Pro (free tier: 2 RPM) for complex Socratic conversations if needed
- **API:** Google AI Studio / Vertex AI with free quota
- **Prompt Management:** Versioned system prompts stored in codebase (not database) for easier testing and iteration
- **Emotion Detection:** Use Gemini API directly (ask "Is user frustrated? Yes/No") rather than separate sentiment analysis library
- **Rate Limiting:** Per-user quotas aligned with free tier limits (10-20 messages/day/user to stay within 1500 requests/day)

**Hosting & Infrastructure:**
- **Hosting:** Azure App Service (Free or Basic tier covered by student/Imagine Cup credits)
- **Database:** Azure Database for PostgreSQL (Basic tier, covered by credits) OR Supabase (free tier)
- **Authentication:** Azure AD B2C (free tier: 50,000 MAU) OR simple JWT-based auth (no external service)
- **Monitoring:** Azure Application Insights (included with App Service)
- **Cost Target:** **$0/month** using Azure free credits + Gemini free tier

**Security & Compliance:**
- **Data Encryption:** HTTPS enforced (TLS 1.3), database encryption at rest (Azure/Supabase default)
- **Input Validation:** Pydantic models for automatic request validation and type checking (backend), Zod for frontend forms
- **Rate Limiting:** slowapi (FastAPI rate limiting library) on API endpoints (prevent abuse, control LLM costs)
- **Password Hashing:** passlib with bcrypt for secure password storage
- **Content Moderation:** better-profanity Python library for profanity filtering in forums
- **GDPR Compliance:** User data export endpoint (JSON download), delete account endpoint (hard delete all related data)
- **No PII beyond email/username:** Don't collect unnecessary personal information

**Development & Deployment:**
- **Version Control:** Git with GitHub
- **Code Quality:**
  - Frontend: ESLint + Prettier
  - Backend: Black (formatter) + Ruff (linter) + mypy (type checking)
  - Pre-commit hooks with pre-commit framework
- **Environment Management:** .env files with pydantic-settings (backend), dotenv (frontend)
- **Deployment Strategy:** Manual deployment via Azure portal OR simple GitHub Actions (if <4 hours setup)
- **Database Migrations:** Alembic for schema migrations

**Cost Optimization:**
- **LLM API:** Aggressive prompt optimization (short system prompts, user message summarization for long conversations)
- **Caching:** Cache common AI responses if patterns emerge
- **Database:** Use connection pooling to minimize database instance size
- **Hosting:** Start with free tiers, Azure credits cover overages

**Timeline-Specific Assumptions:**
- **No custom design system:** Use Tailwind's default theme with minor color customization
- **No complex animations:** CSS transitions only, no Framer Motion or complex libraries
- **No internationalization (i18n):** English-only hardcoded strings for MVP
- **No comprehensive logging infrastructure:** Console.log + basic error tracking only
- **No advanced DevOps:** Manual deployments acceptable if CI/CD setup takes >1 day

---

## Epic List

### Epic 1: Foundation & Authentication
*Establish project infrastructure, deployment pipeline, and user authentication to enable all subsequent development.*

**Goal:** Set up the monorepo, Azure hosting, database, and basic auth so the team can build features on a solid foundation. Deliver a simple "Hello World" landing page as the first deployable increment.

---

### Epic 2: AI-Powered Goal Planning
*Enable users to input goals and receive AI-generated Harada-style plans with editable action steps.*

**Goal:** Allow users to describe their goals in natural language and get back a structured plan they can customize. This delivers the core value proposition of personalized planning.

---

### Epic 3: Socratic Mentor AI & Progress Tracking
*Implement the dual AI system (Mentor + Emotional Support), chat interface, and streak-based progress tracking.*

**Goal:** Enable users to interact with the Socratic Mentor AI that guides without giving answers, detect when users are stuck, and maintain daily streaks to build habit formation. This is the core differentiator of Apollo.

---

### Epic 4: Dynamic Micro-Stepping & Adaptive Scaffolding (P1 - OPTIONAL)
*Build the intelligent system that detects genuine struggle and breaks action steps into 5-10 minute micro-tasks.*

**Goal:** When users are stuck (not lazy), automatically offer micro-stepped guidance that preserves learning while removing overwhelm. This demonstrates Apollo's adaptive scaffolding capability.

**NOTE:** Cut this epic if behind schedule by Dec 23.

---

### Epic 5: Community & Notes (P1 - OPTIONAL)
*Add goal-based forums for peer support and simple note-taking functionality.*

**Goal:** Enable peer community interaction and personal knowledge capture. **CUT THIS EPIC if timeline is tight** - focus on core AI mentor experience.

**NOTE:** Highly cuttable - only implement if Epics 1-3 complete ahead of schedule.

---

## Epic 1: Foundation & Authentication

**Epic Goal:** Establish project infrastructure, Azure deployment pipeline, database schema, and user authentication system. Deliver a working landing page with signup/login functionality, proving the technical stack is operational and the team can deploy to production. This creates the foundation for all feature development while delivering a minimal but complete vertical slice (user can register, log in, and see a dashboard).

### Story 1.1: Initialize Monorepo and Development Environment

**As a** developer,
**I want** a fully configured monorepo with Next.js frontend (TypeScript) and FastAPI backend (Python),
**so that** the team can start building features with consistent tooling and clear separation of concerns.

**Acceptance Criteria:**

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

---

### Story 1.2: Set Up Azure Infrastructure and Database

**As a** developer,
**I want** Azure App Service and PostgreSQL database provisioned and accessible,
**so that** the application can be deployed to production and persist user data.

**Acceptance Criteria:**

1. Azure App Service created (Free or Basic tier) for hosting the FastAPI (Python) backend API
2. Azure Database for PostgreSQL (Basic tier) provisioned with connection string stored in Azure App Service environment variables
3. Database connection verified from local development using connection string (can connect and run basic query)
4. SQLAlchemy installed and configured with Base model class and initial `User` model with fields: id, email, password_hash, created_at, updated_at
5. Alembic initialized for database migrations, initial migration created defining User table
6. Migration successfully applied to Azure PostgreSQL database (`alembic upgrade head`)
7. Database connection pooling configured using SQLAlchemy async engine
8. Azure App Service can connect to database (verified via `/health` endpoint returning database status)

---

### Story 1.3: Implement User Registration and Authentication

**As a** new user,
**I want** to create an account with email and password and log in securely,
**so that** my goals and progress are saved to my personal account.

**Acceptance Criteria:**

1. `/api/auth/register` POST endpoint accepts email and password, validates input (email format, password min 8 chars), hashes password with bcrypt, creates User record in database, returns success response
2. `/api/auth/login` POST endpoint accepts email and password, verifies credentials against database, generates JWT access token (24-hour expiry), returns token in response
3. JWT token includes user ID and email in payload, signed with secret from environment variable
4. `/api/auth/me` GET endpoint requires valid JWT in Authorization header, returns current user's profile (id, email) or 401 Unauthorized if token invalid/missing
5. Password validation prevents common weak passwords (e.g., "password123") using simple rules (min 8 chars, at least 1 number)
6. Duplicate email registration returns 400 error with message "Email already registered"
7. Login with incorrect password returns 401 error without revealing whether email exists (security best practice)

---

### Story 1.4: Build Frontend Authentication UI

**As a** new user,
**I want** a signup and login page with clear forms and error messages,
**so that** I can easily create an account and access the application.

**Acceptance Criteria:**

1. `/signup` page displays form with email input, password input, and "Create Account" button using React Hook Form + Zod validation
2. Signup form validates email format and password requirements (min 8 chars) client-side before submission
3. Successful signup redirects to `/dashboard` and stores JWT token in localStorage (or httpOnly cookie if time permits)
4. Signup errors (duplicate email, validation failures) display as inline error messages below form inputs
5. `/login` page displays form with email input, password input, and "Log In" button
6. Successful login redirects to `/dashboard` and stores JWT token
7. Login errors (incorrect credentials) display generic "Invalid email or password" message (no user enumeration)
8. Both pages include link to switch between signup/login ("Already have an account? Log in" and vice versa)
9. Pages use Tailwind CSS for styling with responsive mobile layout

---

### Story 1.5: Create Protected Dashboard and Deploy to Azure

**As a** logged-in user,
**I want** to see a personalized dashboard after login,
**so that** I know authentication worked and I'm in the application.

**Acceptance Criteria:**

1. `/dashboard` page is protected route that checks for valid JWT token on mount, redirects to `/login` if token missing or expired
2. Dashboard displays "Welcome, [user email]!" message and placeholder content ("Your goals will appear here soon")
3. Dashboard includes "Log Out" button that clears JWT token and redirects to `/login`
4. Frontend makes authenticated API call to `/api/auth/me` to verify token validity and fetch user profile
5. Application deployed to Azure App Service with both frontend and backend accessible via public URL
6. Environment variables configured in Azure App Service (database connection, JWT secret)
7. Deployment pipeline allows team to push updates (manual deploy via Azure portal or Git deployment acceptable for MVP)
8. Public URL loads landing page with "Sign Up" and "Log In" buttons that navigate to respective pages
9. End-to-end flow works in production: User can sign up → log in → see dashboard → log out

---

## Epic 2: AI-Powered Goal Planning

**Epic Goal:** Enable users to input goals in natural language and receive AI-generated Harada-style structured plans with sub-goals and actionable steps. Users can view, edit, and customize their plans. This delivers the first major user-facing value proposition of Apollo - personalized goal planning powered by Gemini AI.

### Story 2.1: Design Database Schema for Goals and Action Steps

**As a** developer,
**I want** a database schema that supports flexible Harada-style goal structures,
**so that** we can store user goals, sub-goals, and action steps with proper relationships.

**Acceptance Criteria:**

1. SQLAlchemy model defines `Goal` class with fields: id, user_id (ForeignKey to User), title, description, status (enum: active, completed, archived), created_at, updated_at
2. SQLAlchemy model defines `SubGoal` class with fields: id, goal_id (ForeignKey to Goal), title, order (integer for sequencing), created_at, updated_at
3. SQLAlchemy model defines `ActionStep` class with fields: id, sub_goal_id (ForeignKey to SubGoal), title, description, status (enum: pending, in_progress, completed), order, estimated_minutes (integer), created_at, updated_at, completed_at (nullable)
4. Database relationships configured: User.goals (one-to-many), Goal.sub_goals (one-to-many), SubGoal.action_steps (one-to-many) with cascade delete
5. Alembic migration created for new models (`alembic revision --autogenerate -m "Add goals schema"`)
6. Migration applied to Azure PostgreSQL database (`alembic upgrade head`)
7. Can create, read, update, delete goals via SQLAlchemy session in backend code (verified with simple test script or pytest)

---

### Story 2.2: Integrate Gemini API for Goal Plan Generation

**As a** developer,
**I want** a backend service that calls Gemini API to generate structured goal plans,
**so that** users can receive AI-powered planning based on their goal description.

**Acceptance Criteria:**

1. Google Generative AI SDK installed and configured with API key from environment variable (`GEMINI_API_KEY`)
2. `generateGoalPlan` service function accepts goal description string and returns structured JSON with format: `{ subGoals: [{ title, actionSteps: [{ title, description, estimatedMinutes }] }] }`
3. System prompt instructs Gemini 1.5 Flash to generate 2-4 sub-goals and 3-6 action steps per sub-goal based on Harada Method principles (flexible structure, actionable steps, realistic sequencing)
4. System prompt emphasizes action steps should be 5-30 minute tasks suitable for daily progress
5. Response parsing handles Gemini JSON output, validates structure, returns error if malformed
6. Error handling catches API failures (rate limit, network error, invalid API key) and returns user-friendly error message
7. Function tested manually with 3-5 example goals (e.g., "Learn Python", "Get fit", "Build a portfolio") and generates reasonable plans

---

### Story 2.3: Build Goal Creation API Endpoint

**As a** logged-in user,
**I want** to submit my goal description and receive a personalized plan,
**so that** I can start working toward my goal with structured guidance.

**Acceptance Criteria:**

1. `POST /api/goals` endpoint requires authentication (valid JWT token), accepts request body: `{ title, description }`
2. Endpoint calls `generateGoalPlan` service with goal description to get AI-generated plan structure
3. Endpoint creates Goal record in database with title, description, and links to authenticated user
4. For each sub-goal in AI response, create SubGoal record linked to Goal with proper order
5. For each action step in AI response, create ActionStep record linked to SubGoal with proper order, status defaulting to "pending"
6. Endpoint returns complete goal structure as JSON including all sub-goals and action steps with IDs
7. Error handling returns 400 if title/description missing, 500 if Gemini API fails, 401 if not authenticated
8. Endpoint respects Gemini rate limiting (if 1500 requests/day quota approaching, return 429 Too Many Requests)

---

### Story 2.4: Create Goal Input and Display UI

**As a** logged-in user,
**I want** a form to describe my goal and see the AI-generated plan,
**so that** I can easily create and visualize my personalized roadmap.

**Acceptance Criteria:**

1. Dashboard includes "+ Create New Goal" button that navigates to `/goals/new` page
2. `/goals/new` page displays form with "Goal Title" input (max 100 chars) and "Describe your goal" textarea (max 500 chars) with character counters
3. Form includes "Generate My Plan" button that calls `POST /api/goals` with form data
4. During API call, button shows loading state ("Generating plan...") and is disabled to prevent duplicate submissions
5. On success, redirect to `/goals/[goalId]` showing the newly created goal with full plan structure
6. `/goals/[goalId]` page displays goal title, description, and expandable/collapsible list of sub-goals
7. Each sub-goal shows title and nested list of action steps with titles and estimated time
8. Action steps display with checkbox (not interactive yet, placeholder for future progress tracking)
9. Error messages display if API call fails (e.g., "Could not generate plan. Please try again.")
10. Page uses Tailwind CSS with clean, readable layout (card-based design for sub-goals)

---

### Story 2.5: Implement Goal Editing and Deletion

**As a** logged-in user,
**I want** to modify my goal plan if the AI-generated steps aren't quite right,
**so that** I can customize the plan to fit my actual situation and capabilities.

**Acceptance Criteria:**

1. `PATCH /api/goals/:goalId` endpoint allows authenticated user to update goal title and description (only if goal belongs to user, else 403 Forbidden)
2. `DELETE /api/goals/:goalId` endpoint allows authenticated user to delete goal and cascade-delete all sub-goals and action steps (only if goal belongs to user)
3. `PATCH /api/action-steps/:stepId` endpoint allows user to update action step title, description, and estimatedMinutes
4. `DELETE /api/action-steps/:stepId` endpoint allows user to delete individual action step
5. Goal detail page (`/goals/[goalId]`) includes "Edit Goal" button that opens inline edit mode or modal with title/description inputs
6. Saving edits calls PATCH endpoint and updates UI optimistically (shows changes immediately, reverts if API fails)
7. Goal detail page includes "Delete Goal" button with confirmation dialog ("Are you sure? This cannot be undone")
8. Each action step has "Edit" icon/button that allows inline editing of title and estimated time
9. Changes persist to database and reload correctly when user navigates away and returns to goal page
10. Dashboard (`/dashboard`) now shows list of all user's active goals with titles and "View" link to goal detail page

---

### Story 2.6: Add Goal List and Dashboard Overview

**As a** logged-in user,
**I want** to see all my active goals on the dashboard,
**so that** I can quickly access any goal and track my overall progress.

**Acceptance Criteria:**

1. `GET /api/goals` endpoint returns all goals for authenticated user with basic info (id, title, status, progress percentage calculated as completed steps / total steps)
2. Dashboard displays goal cards in grid layout (responsive: 1 column mobile, 2-3 columns desktop)
3. Each goal card shows goal title, progress bar (0-100%), and "View Details" button linking to `/goals/[goalId]`
4. If user has no goals, dashboard shows empty state with "+ Create Your First Goal" button
5. Dashboard shows placeholder for future features: "🔥 Current Streak: 0 days" (not functional yet, coming in Epic 3)
6. Goal cards use distinct visual styling (border, shadow, hover effect) to feel interactive
7. Goals are sorted by createdAt descending (newest goals first)
8. Clicking anywhere on goal card (not just button) navigates to goal detail page

---

## Epic 3: Socratic Mentor AI & Progress Tracking

**Epic Goal:** Implement the dual AI system (Socratic Mentor AI + Emotional Support AI) with chat interface, intelligent context switching based on user emotion/progress, and streak-based progress tracking. This delivers Apollo's unique value proposition: an AI that guides users to find answers themselves rather than giving direct solutions, combined with habit-forming streak mechanics.

### Story 3.1: Extend Database Schema for Progress and Chat

**As a** developer,
**I want** database models for tracking action step completion, streaks, and AI chat conversations,
**so that** we can persist user progress and conversation history.

**Acceptance Criteria:**

1. SQLAlchemy `User` model updated with additional fields: current_streak (Integer, default 0), longest_streak (Integer, default 0), last_active_date (DateTime, nullable)
2. SQLAlchemy `ActionStep` model adds field: completed_at (DateTime, nullable) to track when step was completed
3. SQLAlchemy model defines `ChatMessage` class with fields: id, user_id, goal_id (nullable, ForeignKey), action_step_id (nullable, ForeignKey), role (enum: user, mentor, emotional_support), content (Text), timestamp (DateTime)
4. SQLAlchemy model defines `UserProgress` class with fields: id, user_id (ForeignKey), date (Date, unique constraint with user_id), actions_completed (Integer), minutes_worked (Integer)
5. Alembic migration created for schema changes (`alembic revision --autogenerate -m "Add progress tracking and chat"`)
6. Migration applied to Azure PostgreSQL (`alembic upgrade head`)
7. Can create chat messages and update progress via SQLAlchemy session (verified with test script or pytest)

---

### Story 3.2: Build Socratic Mentor AI Service

**As a** developer,
**I want** a backend service that implements Socratic questioning using Gemini,
**so that** the AI guides users without giving direct answers.

**Acceptance Criteria:**

1. `socraticMentor` service function accepts user message, conversation history, and current goal/action step context
2. System prompt instructs Gemini to act as Socratic mentor: ask guiding questions, never provide direct answers/solutions/code, help user think through problems themselves
3. System prompt includes explicit examples of Socratic responses vs. prohibited direct answers (e.g., "What have you tried so far?" vs. "Here's the solution: ...")
4. System prompt includes user's current action step context to keep questions relevant
5. Function calls Gemini 1.5 Flash API with conversation history (last 10 messages max to control token usage)
6. Response is validated to ensure it doesn't contain direct answers (basic keyword detection: no code blocks, no step-by-step solutions) - if detected, re-prompt with stronger Socratic enforcement
7. Function returns Gemini response and logs conversation to database (ChatMessage with role: mentor)
8. Manually tested with 10 scenarios (user asking "how do I...", "what is...", etc.) and confirms AI asks questions back at least 70% of the time

---

### Story 3.3: Build Emotional Support AI Service

**As a** developer,
**I want** a backend service that detects user frustration and provides encouragement,
**so that** users feel supported when genuinely stuck.

**Acceptance Criteria:**

1. `emotionalSupport` service function accepts user message and recent progress history (action steps completed in last 7 days)
2. System prompt instructs Gemini to act as empathetic coach: validate feelings, provide encouragement, suggest taking breaks or switching tasks if user seems overwhelmed
3. `detectFrustration` helper function analyzes user message for frustration signals using Gemini: asks "Is the user expressing frustration, confusion, or feeling stuck? Answer: Yes/No/Unsure" and parses response
4. Frustration detection considers progress history: if user hasn't completed steps in 3+ days AND message contains negative language, likely frustrated
5. When frustration detected, function triggers emotional support mode and offers encouragement with specific acknowledgment of their struggle
6. Function returns supportive response and logs to database (ChatMessage with role: emotional_support)
7. Manually tested with 5 frustrated user messages (e.g., "I don't understand this", "This is too hard", "I've been stuck for days") and confirms empathetic responses

---

### Story 3.4: Implement AI Chat API Endpoint with Context Switching

**As a** logged-in user,
**I want** to chat with the AI mentor about my current action step,
**so that** I can get guidance when I'm unsure how to proceed.

**Acceptance Criteria:**

1. `POST /api/chat` endpoint requires authentication, accepts request body: `{ message, goalId, actionStepId (optional) }`
2. Endpoint retrieves conversation history (last 10 ChatMessages for this user + goal)
3. Endpoint calls `detectFrustration` function to determine user emotional state
4. If frustration detected AND user hasn't completed steps recently, call `emotionalSupport` service
5. Otherwise, call `socraticMentor` service with goal/action step context
6. Response includes: `{ reply, aiMode: 'mentor' | 'emotional_support' }` so frontend can differentiate
7. Endpoint saves both user message and AI response to ChatMessage table
8. Error handling catches Gemini API failures and returns fallback message: "I'm having trouble connecting right now. Please try again in a moment."
9. Endpoint respects rate limiting (max 20 messages per user per day for MVP to stay within Gemini quota)

---

### Story 3.5: Build AI Chat Interface UI

**As a** logged-in user,
**I want** a chat interface on my goal page where I can ask questions about my action steps,
**so that** I can get Socratic guidance when I'm unsure how to proceed.

**Acceptance Criteria:**

1. Goal detail page (`/goals/[goalId]`) includes collapsible "💬 Chat with Mentor" section
2. Chat section displays conversation history with user messages aligned right (blue) and AI messages aligned left (gray/green)
3. AI messages show subtle indicator of mode: "🤔 Mentor" for Socratic mode, "💙 Support" for emotional support mode
4. Chat input textarea at bottom with "Send" button, supports Enter key to submit (Shift+Enter for new line)
5. During API call, input is disabled and "Sending..." loading indicator appears
6. New messages appear in chat instantly (optimistic UI) and scroll to bottom automatically
7. If user hasn't selected an action step, chat shows message: "Tip: Select an action step you're working on for more focused guidance"
8. Action steps in goal view now clickable - clicking sets active action step and updates chat context (shows "Currently working on: [step title]" above chat)
9. Chat persists across page refreshes (loads conversation history from API on mount)
10. Mobile responsive: chat section takes full width, messages stack vertically

---

### Story 3.6: Implement Action Step Completion and Streak Tracking

**As a** logged-in user,
**I want** to mark action steps as complete and see my daily streak,
**so that** I feel motivated to work on my goals consistently.

**Acceptance Criteria:**

1. `POST /api/action-steps/:stepId/complete` endpoint marks action step as completed (status: completed, completedAt: now)
2. Endpoint updates UserProgress record for today: increments actionsCompleted, adds estimatedMinutes to minutesWorked (creates record if first action of the day)
3. Endpoint updates User streak: if lastActiveDate was yesterday, increment currentStreak; if today, do nothing; if gap >1 day, reset currentStreak to 1 and update longestStreak if needed
4. Endpoint returns updated action step and new streak count
5. Action steps on goal detail page have checkbox that when clicked calls completion endpoint and updates UI (checkbox checked, step gets strikethrough styling)
6. Completed steps can be unchecked (calls `POST /api/action-steps/:stepId/uncomplete`) to revert completion
7. Dashboard shows "🔥 Current Streak: X days" prominently at top (X = user.currentStreak)
8. Dashboard shows "Actions completed today: X" (X = today's UserProgress.actionsCompleted or 0)
9. Streak resets to 0 if user goes 2+ days without completing any action steps (checked via background job or on next login)
10. Celebration UI: When user completes action step, show brief success message: "✅ Nice work! Keep going!" (toast notification or inline message)

---

### Story 3.7: Add Daily Check-In Prompt

**As a** logged-in user,
**I want** a daily check-in prompt when I log in,
**so that** I'm encouraged to choose what to work on and stay focused.

**Acceptance Criteria:**

1. When user loads dashboard, check if they've completed any actions today (query UserProgress for today's date)
2. If no actions completed today AND user has active goals, show modal/banner: "What are you working on today?"
3. Modal lists user's active goals with next incomplete action step for each goal
4. User can click an action step to navigate to that goal's detail page with the action step pre-selected
5. Modal includes "I'll decide later" button to dismiss without selecting
6. Check-in modal only appears once per day (track in localStorage or session storage that user saw it)
7. If user has no active goals, check-in shows: "Ready to start? Create your first goal!" with link to goal creation page
8. Check-in is non-blocking (user can close it and still access dashboard normally)

---

## Epic 4: Dynamic Micro-Stepping & Adaptive Scaffolding (P1 - OPTIONAL)

**Epic Goal:** Build the intelligent system that detects when users are genuinely stuck (not lazy) and automatically breaks down overwhelming action steps into 5-10 minute micro-steps. This demonstrates Apollo's adaptive scaffolding capability - preserving user agency and learning while removing unproductive friction.

**NOTE:** This epic is P1 (nice-to-have). Cut if behind schedule by Dec 23.

### Story 4.1: Extend Database Schema for Micro-Steps

**As a** developer,
**I want** database models for storing micro-steps and stuck detection metadata,
**so that** we can track when scaffolding is offered and how users engage with it.

**Acceptance Criteria:**

1. SQLAlchemy model defines `MicroStep` class with fields: id, action_step_id (ForeignKey), title, order (Integer), status (enum: pending, completed), completed_at (DateTime, nullable), created_at (DateTime)
2. SQLAlchemy `ActionStep` model adds fields: micro_steps_generated (Boolean, default False), stuck_detected_at (DateTime, nullable), micro_step_exited_at (DateTime, nullable)
3. SQLAlchemy `ChatMessage` model adds field: triggered_micro_stepping (Boolean, default False) to track when conversation led to scaffolding
4. Alembic migration created and applied (`alembic revision --autogenerate` then `alembic upgrade head`)
5. Can create micro-steps and update action step flags via SQLAlchemy session

---

### Story 4.2: Build Stuck Detection Service

**As a** developer,
**I want** a service that identifies when users are genuinely stuck vs. lazy,
**so that** we only offer scaffolding when it's truly needed.

**Acceptance Criteria:**

1. `detectStuck` service function accepts: user message, action step, progress history (last 14 days), chat history (last 10 messages)
2. Function uses Gemini to analyze whether user is genuinely stuck based on criteria: repeated questions about same action step (3+ messages without progress), negative sentiment in messages, action step incomplete for 3+ days, user explicitly says "I'm stuck" or similar
3. Function distinguishes "stuck" from "lazy" by checking: if user completed other steps recently (active elsewhere = likely genuinely stuck on this one), if user is asking specific questions (engagement signal), if time estimate for step is unrealistic given user's context
4. Returns stuck assessment: `{ isStuck: boolean, confidence: 'high' | 'medium' | 'low', reason: string }`
5. If confidence is 'high' and isStuck is true, triggers micro-stepping offer
6. Manually tested with 5 "stuck" scenarios and 5 "lazy" scenarios, correctly identifies at least 7/10

---

### Story 4.3: Build Micro-Step Generation Service

**As a** developer,
**I want** a service that breaks action steps into 5-10 minute micro-tasks using Gemini,
**so that** overwhelming steps become manageable for stuck users.

**Acceptance Criteria:**

1. `generateMicroSteps` service function accepts action step (title, description, estimatedMinutes) and goal context
2. System prompt instructs Gemini to break action step into 3-8 micro-steps, each completable in 5-10 minutes, with very specific and concrete tasks
3. System prompt emphasizes micro-steps should be sequential (step 2 builds on step 1) and require no prerequisite knowledge user hasn't demonstrated
4. Function calls Gemini 1.5 Flash with action step context
5. Response parsed into array of micro-step titles: `[{ title, order }]`
6. Function creates MicroStep records in database linked to action step and returns array
7. Action step updated: microStepsGenerated = true, stuckDetectedAt = now
8. Manually tested with 3 complex action steps (e.g., "Set up development environment", "Write first function", "Deploy to cloud") and generates reasonable 5-10 min breakdowns

---

### Story 4.4: Implement Micro-Stepping Offer in Chat

**As a** logged-in user,
**I want** the AI to detect when I'm stuck and offer to break down the step for me,
**so that** I get help when I need it without having to explicitly ask.

**Acceptance Criteria:**

1. Chat API endpoint (`POST /api/chat`) now includes stuck detection check after receiving user message
2. If `detectStuck` returns high confidence stuck status, AI response includes offer: "It seems like this step might be challenging. Would you like me to break it down into smaller 5-10 minute tasks?"
3. User can respond "yes" or click suggested action button "Break it down" (detected via message parsing or explicit button payload)
4. When user accepts, endpoint calls `generateMicroSteps` service and returns micro-step list in response
5. Chat interface displays micro-steps as interactive checklist within the conversation (not just text list)
6. User can mark micro-steps complete inline in chat (calls new `POST /api/micro-steps/:id/complete` endpoint)
7. When all micro-steps are completed, AI congratulates user and suggests marking the parent action step as complete
8. User can decline offer ("No thanks, I'll keep trying") - AI responds supportively and continues Socratic questioning
9. Stuck detection only triggers once per action step per 24 hours to avoid annoying user with repeated offers

---

### Story 4.5: Build Micro-Step Completion and Exit UI

**As a** logged-in user,
**I want** to work through micro-steps and exit scaffolding when I'm ready,
**so that** I maintain control over my learning process.

**Acceptance Criteria:**

1. When micro-steps are generated for an action step, goal detail page shows "🎯 Scaffolding Active" badge on that action step
2. Clicking action step expands inline view showing list of micro-steps with checkboxes
3. Checking micro-step checkbox calls `POST /api/micro-steps/:id/complete` and updates UI (strikethrough, timestamp)
4. Micro-step view includes "Exit Scaffolding" button that collapses micro-steps and returns to normal action step view
5. Clicking "Exit Scaffolding" updates action step: microStepExitedAt = now, hides micro-steps (still in DB but not shown)
6. If user exits scaffolding and becomes stuck again later, system can re-offer or generate new micro-steps (not just show old ones)
7. Progress calculation: Action step counts as complete only if parent action step is marked complete OR all micro-steps are completed
8. Streak tracking: Completing micro-steps counts toward daily actions completed (each micro-step increments counter)
9. Mobile responsive: Micro-step checklist stacks vertically with clear touch targets

---

### Story 4.6: Add Scaffolding Analytics and Feedback

**As a** product team,
**I want** basic analytics on scaffolding usage and effectiveness,
**so that** we can demonstrate the adaptive learning concept to competition judges.

**Acceptance Criteria:**

1. Database query to count: total users who received micro-stepping offer, acceptance rate, completion rate of micro-steps vs. parent action steps
2. Simple admin dashboard or script (`npm run analytics`) that outputs scaffolding metrics: offers made, accepted, declined, micro-steps completed, action steps completed via scaffolding
3. After user completes all micro-steps, AI asks: "How did breaking this down help? (Just curious!)" - captures qualitative feedback in chat
4. Feedback stored in ChatMessage and can be manually reviewed for testimonials
5. Metrics visible in simple markdown report (generated by script) for inclusion in competition pitch deck: "X% of stuck users accepted scaffolding, Y% completed their action step with our help"
6. No fancy dashboard UI needed - command-line output or markdown file sufficient for MVP

---

## Epic 5: Community & Notes (P1 - OPTIONAL)

**Epic Goal:** Add goal-based community forums for peer support and simple note-taking functionality. This addresses the "loss of human interaction" problem by enabling users to connect with others working on similar goals and capture their learning insights. **CUT THIS ENTIRE EPIC if behind schedule on Dec 23** - Epics 1-4 deliver the core Apollo value proposition.

**NOTE:** This epic is highly cuttable. Only implement if ahead of schedule.

### Story 5.1: Design Database Schema for Forums and Notes

**As a** developer,
**I want** database models for forum posts, replies, and user notes,
**so that** we can persist community content and personal reflections.

**Acceptance Criteria:**

1. SQLAlchemy model defines `Forum` class with fields: id, title (e.g., "Learning Python", "Getting Fit"), slug (String, URL-friendly), description (Text), created_at (DateTime)
2. SQLAlchemy model defines `ForumPost` class with fields: id, forum_id (ForeignKey), user_id (ForeignKey), title, content (Text), upvotes (Integer, default 0), created_at, updated_at
3. SQLAlchemy model defines `ForumReply` class with fields: id, post_id (ForeignKey to ForumPost), user_id (ForeignKey), content (Text), created_at
4. SQLAlchemy model defines `Note` class with fields: id, user_id (ForeignKey), goal_id (ForeignKey), content (Text, markdown), created_at, updated_at
5. Alembic migration created and applied for all forum and note models
6. Can create forums, posts, replies, and notes via SQLAlchemy session

---

### Story 5.2: Implement Forum Creation and Post Management APIs

**As a** developer,
**I want** backend APIs for creating forums, posting, replying, and upvoting,
**so that** users can participate in goal-based communities.

**Acceptance Criteria:**

1. `GET /api/forums` endpoint returns list of all forums (public, no auth required)
2. `POST /api/forums` endpoint creates new forum (title, description) - admin/system only for MVP (hardcode check or skip auth), auto-generates slug from title
3. `GET /api/forums/:slug/posts` endpoint returns posts for forum sorted by upvotes descending, includes author email (for display), post count
4. `POST /api/forums/:slug/posts` endpoint creates post (requires auth, validates title and content not empty)
5. `POST /api/posts/:postId/upvote` endpoint increments post upvotes (requires auth, one upvote per user - store in separate UpVote join table or allow multiple for MVP simplicity)
6. `GET /api/posts/:postId/replies` endpoint returns replies for post with author info
7. `POST /api/posts/:postId/replies` endpoint creates reply (requires auth, validates content not empty)
8. Basic profanity filter applied to all post/reply content before saving (using bad-words library)
9. Error handling for invalid forum slugs, missing posts, unauthorized access

---

### Story 5.3: Build Forum Browse and Post UI

**As a** logged-in user,
**I want** to browse forums related to my goals and post questions or progress updates,
**so that** I can connect with peers working on similar objectives.

**Acceptance Criteria:**

1. Navigation header includes "Community" link that navigates to `/forums` page
2. `/forums` page displays grid of forum cards with title, description, and post count (e.g., "Learning Python - 42 posts")
3. Clicking forum card navigates to `/forums/[slug]` showing list of posts sorted by upvotes
4. Forum page includes "+ New Post" button (only visible if logged in) that opens post creation form
5. Post creation form has title input, content textarea (supports basic markdown), "Post" button
6. Posts display as cards showing: title, first 150 chars of content, upvote count with upvote button (↑), reply count, author email, timestamp
7. Upvote button calls API and updates count optimistically (increments immediately, reverts if API fails)
8. Clicking post card navigates to `/forums/[slug]/posts/[postId]` showing full post + replies
9. Post detail page displays full markdown-rendered content, upvote button, reply form at bottom
10. Reply form is simple textarea with "Reply" button, replies display chronologically below post
11. Mobile responsive: Cards stack vertically, forms take full width

---

### Story 5.4: Auto-Create Forums Based on User Goals

**As a** user creating goals,
**I want** forums to automatically exist for my goal categories,
**so that** I can immediately find relevant communities.

**Acceptance Criteria:**

1. When user creates goal via `POST /api/goals`, backend extracts goal category from title/description using Gemini (ask "What category is this goal? Options: Learning/Programming, Fitness/Health, Career/Professional, Creative/Arts, Personal/Habits, Other")
2. System checks if forum for that category already exists (by slug), creates new forum if not found
3. Goal record includes optional `forumId` field linking to relevant forum
4. Goal detail page shows "💬 Join the [Category] Community" link to relevant forum if forumId exists
5. Forums page shows "Recommended for You" section at top highlighting forums matching user's active goal categories
6. If Gemini categorization fails, default to generic "General Goals" forum
7. Maximum 20 forums to avoid fragmentation (if category doesn't match existing 20, assign to closest match or "Other")

---

### Story 5.5: Implement Note-Taking Functionality

**As a** logged-in user,
**I want** to capture insights and reflections as I work on my goals,
**so that** I can build a personal knowledge base and track my learning.

**Acceptance Criteria:**

1. `POST /api/goals/:goalId/notes` endpoint creates note (requires auth, content is markdown text)
2. `GET /api/goals/:goalId/notes` endpoint returns all notes for goal sorted by createdAt descending
3. `PATCH /api/notes/:noteId` endpoint updates note content (only if note belongs to authenticated user)
4. `DELETE /api/notes/:noteId` endpoint deletes note (only if belongs to user)
5. Goal detail page includes "📝 Notes" collapsible section below chat
6. Notes section displays existing notes as cards with timestamp, edit/delete icons
7. "+ Add Note" button opens markdown editor (simple textarea with preview toggle)
8. Editor supports basic markdown: headings, bold, italic, lists, links (use react-markdown for rendering)
9. Notes auto-save on blur or have explicit "Save" button (debounced to avoid excessive API calls)
10. Notes are private to user (not visible to others, no sharing for MVP)

---

### Story 5.6: Add Content Moderation and Community Guidelines

**As a** product team,
**I want** basic content moderation to prevent spam and abuse in forums,
**so that** the community remains supportive and safe.

**Acceptance Criteria:**

1. Profanity filter applied to all forum posts and replies before saving (already in Story 5.2)
2. `/community-guidelines` page with simple rules: Be respectful, No spam, Support others, Stay on topic
3. Post/reply forms include checkbox: "I agree to community guidelines" (required before submission)
4. Rate limiting on forum posts: Max 10 posts per user per day, max 20 replies per user per day
5. "Report" button on posts/replies (for future moderation, just logs to database for MVP - no action taken)
6. Admin can manually delete posts/replies via direct database access (no UI needed for MVP)
7. If user's post is rejected by profanity filter, show error: "Your post contains inappropriate language. Please revise and try again."

---

## Checklist Results Report

### Executive Summary

**Overall PRD Completeness:** 92%
**MVP Scope Appropriateness:** Just Right (aggressive but achievable with timeline awareness)
**Readiness for Architecture Phase:** Ready

**Most Critical Concerns:**
- No formal user research conducted yet (assumptions based on competition theme)
- Socratic AI quality metrics are manual/subjective (75% target based on aspiration, not validation)
- Timeline is aggressive (20 development days for 30 stories) - requires ruthless prioritization
- Gemini free tier quota management critical (1500 req/day limit could be hit with 75+ active users)

### Category Statuses

| Category                         | Status  | Critical Issues |
| -------------------------------- | ------- | --------------- |
| 1. Problem Definition & Context  | PASS    | User research is assumed, not validated |
| 2. MVP Scope Definition          | PASS    | Epic 5 properly flagged as cuttable, scope well-bounded |
| 3. User Experience Requirements  | PASS    | Core flows documented, accessibility specified (WCAG AA) |
| 4. Functional Requirements       | PASS    | 18 FRs cover all MVP features, testable and specific |
| 5. Non-Functional Requirements   | PASS    | 16 NFRs corrected for MVP (Gemini, Azure credits, manual testing) |
| 6. Epic & Story Structure        | PASS    | 30 stories across 5 epics, properly sequenced, P0/P1 marked |
| 7. Technical Guidance            | PASS    | Gemini + Azure stack specified, monorepo + modular monolith chosen |
| 8. Cross-Functional Requirements | PARTIAL | No explicit data migration plan, minimal operational monitoring |
| 9. Clarity & Communication       | PASS    | Clear language, consistent terminology, well-structured |

**Overall Status:** READY FOR ARCHITECT (with minor clarifications)

### Top Recommendations

**Before Architect Handoff:**
1. **Clarify PWA Scope:** Make PWA P1 - web responsive is P0, installable/offline is nice-to-have
2. **Auth Implementation:** Recommend DIY JWT for MVP (saves setup time), migrate to Azure AD B2C post-competition if needed
3. **Socratic AI Baseline:** Test Gemini Socratic capability with 5 sample prompts BEFORE building full service

**During Development:**
4. **Daily Gemini Quota Check:** Monitor daily request count vs. 1500 limit, alert at 1200 (80%)
5. **Epic 3 Extra Time:** Allocate 6 days (not 5) for Epic 3 - Socratic AI prompt iteration is unpredictable
6. **Dec 20 Checkpoint:** Hard stop on Dec 20 to assess progress. If Epic 3 incomplete, immediately cut Epic 4-5

### Final Decision

✅ **READY FOR ARCHITECT**

The PRD and epic definitions are comprehensive, properly structured, and ready for architectural design. Minor clarifications needed (PWA scope, auth approach) can be resolved during architecture phase. No blockers to proceeding.

---

## Next Steps

### UX Expert Prompt

```
I need you to review the Apollo PRD and create a comprehensive UI/UX design specification.

Context:
- Product: Apollo - AI-powered Socratic goal mentor for learners
- Competition: Microsoft Imagine Cup 2025 (deadline: Dec 28)
- Timeline: 24 days total, need designs by Dec 17 (Day 3)
- Tech: Next.js + Tailwind CSS, web-responsive (desktop + mobile)
- MVP Focus: Speed over polish, functional design prioritized

Key Screens to Design (Priority Order):
1. Dashboard (home page with goals list, streak counter)
2. Goal Creation (form + AI-generated plan display)
3. Goal Detail View (action steps, AI chat interface, progress)
4. AI Chat Interface (conversational UI with Mentor/Emotional modes)
5. Signup/Login pages (simple, clean auth forms)

Design Constraints:
- WCAG AA accessibility (contrast, keyboard nav, screen readers)
- Mobile-first responsive (320px-1280px+ breakpoints)
- Minimal animation/transitions (faster development)
- Tailwind CSS utility classes (no custom design system)
- Calm, encouraging tone (not gamified or urgent)

Deliverables Needed:
1. Wireframes for 5 core screens (low-fidelity acceptable)
2. Component specifications (buttons, forms, cards, chat bubbles)
3. Color palette (primary, accent, neutral, success/error states)
4. Typography choices (font families, sizes, weights)
5. Interaction patterns (how chat works, how streaks display, how micro-steps expand)

Please read the full PRD at docs/prd.md and generate the UI/UX design specification.
```

### Architect Prompt

```
I need you to design the technical architecture for Apollo based on the PRD.

Context:
- Product: Apollo - AI-powered Socratic goal mentor platform
- Competition: Microsoft Imagine Cup 2025 (deadline: Dec 28, 2025)
- Timeline: 24 days total, architecture needed by Dec 15 (Day 1-2)
- Team: 3 developers (full-stack capable)
- Budget: $0/month using Gemini free tier + Azure student credits

Technical Stack (Decided):
- Frontend: Next.js 14+ (App Router), TypeScript, Tailwind CSS
- Backend: FastAPI (Python 3.11+), Pydantic for validation
- Database: Azure PostgreSQL (Basic tier) or Supabase
- ORM: SQLAlchemy 2.0+ with async support, Alembic for migrations
- AI: Google Gemini 1.5 Flash (free tier: 1500 req/day)
- Hosting: Azure App Service (covered by credits)
- Architecture: Monorepo (frontend + backend folders), Modular Monolith

Key Architecture Challenges:
1. Socratic AI Implementation: System prompts that reliably refuse direct answers (75%+ success rate target)
2. Stuck Detection Algorithm: Multi-signal heuristic (chat sentiment + progress history + time + engagement)
3. Gemini Quota Management: Stay within 1500 requests/day, rate limit users
4. Real-time Consideration: Forums need updates within 5 seconds (WebSocket vs. polling tradeoff)
5. Streak Calculation: Efficient daily progress tracking without background jobs
6. Auth Decision: DIY JWT vs. Azure AD B2C vs. Supabase Auth (evaluate setup time vs. security)

Critical Requirements:
- AI response time <3 seconds (P95)
- Deployable to Azure by Day 3 (Dec 17)
- Database schema supports flexible Harada-style goals (variable sub-goals and action steps)
- SQLAlchemy ORM with Pydantic models for type-safe database and API access
- Python async/await for concurrent request handling
- No E2E test automation (manual QA sufficient for MVP)

Deliverables Needed:
1. System architecture diagram (components, data flow, integrations)
2. Database schema (SQLAlchemy models for User, Goal, SubGoal, ActionStep, ChatMessage, UserProgress, MicroStep, Forum, ForumPost, ForumReply, Note)
3. API endpoint design (FastAPI routers with Pydantic request/response schemas)
4. Gemini integration architecture (prompt management, response parsing, error handling, quota tracking)
5. Deployment strategy (Azure App Service setup for Python, environment variables, CI/CD approach)
6. Technical risk mitigation (Socratic AI validation, Azure Python runtime setup, async database connection pooling)

Please read the full PRD at docs/prd.md and design the technical architecture.
```

---

**🎉 PRD Complete! Total: 30 stories across 5 epics, ready for Dec 28 competition deadline.**
