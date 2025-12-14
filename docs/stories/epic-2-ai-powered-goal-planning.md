# Epic 2: AI-Powered Goal Planning

**Project:** Apollo
**Epic Goal:** Enable users to input goals in natural language and receive AI-generated Harada-style structured plans with sub-goals and actionable steps. Users can view, edit, and customize their plans. This delivers the first major user-facing value proposition of Apollo - personalized goal planning powered by Gemini AI.

**Priority:** P0 (Must Have)
**Estimated Timeline:** Days 6-10 of development
**Dependencies:** Epic 1 (Foundation & Authentication)

---

## Story 2.1: Design Database Schema for Goals and Action Steps

**As a** developer,
**I want** a database schema that supports flexible Harada-style goal structures,
**so that** we can store user goals, sub-goals, and action steps with proper relationships.

### Acceptance Criteria

1. SQLAlchemy model defines `Goal` class with fields: id, user_id (ForeignKey to User), title, description, status (enum: active, completed, archived), created_at, updated_at
2. SQLAlchemy model defines `SubGoal` class with fields: id, goal_id (ForeignKey to Goal), title, order (integer for sequencing), created_at, updated_at
3. SQLAlchemy model defines `ActionStep` class with fields: id, sub_goal_id (ForeignKey to SubGoal), title, description, status (enum: pending, in_progress, completed), order, estimated_minutes (integer), created_at, updated_at, completed_at (nullable)
4. Database relationships configured: User.goals (one-to-many), Goal.sub_goals (one-to-many), SubGoal.action_steps (one-to-many) with cascade delete
5. Alembic migration created for new models (`alembic revision --autogenerate -m "Add goals schema"`)
6. Migration applied to Azure PostgreSQL database (`alembic upgrade head`)
7. Can create, read, update, delete goals via SQLAlchemy session in backend code (verified with simple test script or pytest)

### Technical Notes

- **Database Models:** Goal, SubGoal, ActionStep
- **ORM:** SQLAlchemy 2.0.28 with async support
- **Migrations:** Alembic 1.13.0
- **Relationships:** One-to-many with cascade delete for referential integrity

### Database Schema

**Goal Model**
```python
class Goal(Base):
    __tablename__ = "goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum("active", "completed", "archived", name="goal_status"), default="active", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="goals")
    sub_goals = relationship("SubGoal", back_populates="goal", cascade="all, delete-orphan")
```

**SubGoal Model**
```python
class SubGoal(Base):
    __tablename__ = "sub_goals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    goal = relationship("Goal", back_populates="sub_goals")
    action_steps = relationship("ActionStep", back_populates="sub_goal", cascade="all, delete-orphan")
```

**ActionStep Model**
```python
class ActionStep(Base):
    __tablename__ = "action_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sub_goal_id = Column(UUID(as_uuid=True), ForeignKey("sub_goals.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(Enum("pending", "in_progress", "completed", name="action_step_status"), default="pending", nullable=False)
    order = Column(Integer, nullable=False)
    estimated_minutes = Column(Integer, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    sub_goal = relationship("SubGoal", back_populates="action_steps")
```

### Definition of Done

- [ ] Goal, SubGoal, and ActionStep models defined in SQLAlchemy
- [ ] Relationships configured with cascade delete
- [ ] Alembic migration created and applied to database
- [ ] Models tested with CRUD operations
- [ ] Database indexes created on foreign keys

---

## Story 2.2: Integrate Gemini API for Goal Plan Generation

**As a** developer,
**I want** a backend service that calls Gemini API to generate structured goal plans,
**so that** users can receive AI-powered planning based on their goal description.

### Acceptance Criteria

1. Google Generative AI SDK installed and configured with API key from environment variable (`GEMINI_API_KEY`)
2. `generateGoalPlan` service function accepts goal description string and returns structured JSON with format: `{ subGoals: [{ title, actionSteps: [{ title, description, estimatedMinutes }] }] }`
3. System prompt instructs Gemini 1.5 Flash to generate 2-4 sub-goals and 3-6 action steps per sub-goal based on Harada Method principles (flexible structure, actionable steps, realistic sequencing)
4. System prompt emphasizes action steps should be 5-30 minute tasks suitable for daily progress
5. Response parsing handles Gemini JSON output, validates structure, returns error if malformed
6. Error handling catches API failures (rate limit, network error, invalid API key) and returns user-friendly error message
7. Function tested manually with 3-5 example goals (e.g., "Learn Python", "Get fit", "Build a portfolio") and generates reasonable plans

### Technical Notes

- **AI Service:** Google Gemini 1.5 Flash API
- **SDK:** google-generativeai 0.4.0 (Python SDK)
- **Rate Limit:** 15 RPM, 1M TPM, 1500 requests/day (free tier)
- **Timeout:** 10 seconds on all Gemini API calls
- **Error Handling:** Retry once with 2s backoff for transient failures

### System Prompt Template

```python
GOAL_PLANNING_PROMPT = """You are an expert goal planning assistant using the Harada Method.
Given a user's goal description, create a structured plan with:

1. 2-4 sub-goals (intermediate milestones toward the main goal)
2. For each sub-goal, 3-6 action steps (specific, actionable tasks)

Requirements for action steps:
- Each step should take 5-30 minutes to complete
- Steps should be concrete and measurable
- Steps should be sequenced logically
- Use clear, action-oriented language
- Estimate realistic time in minutes

Return ONLY valid JSON in this exact format:
{
  "subGoals": [
    {
      "title": "Sub-goal title",
      "actionSteps": [
        {
          "title": "Action step title",
          "description": "Detailed description of what to do",
          "estimatedMinutes": 15
        }
      ]
    }
  ]
}

User's goal: {goal_description}
"""
```

### Service Function

```python
async def generateGoalPlan(goal_description: str) -> dict:
    """
    Generate a Harada-style goal plan using Gemini API.

    Args:
        goal_description: User's natural language goal description

    Returns:
        Dictionary with structure: { subGoals: [...] }

    Raises:
        GeminiAPIError: If API call fails
        ValidationError: If response format is invalid
    """
```

### Definition of Done

- [ ] Google Generative AI SDK installed and configured
- [ ] `generateGoalPlan` service function implemented
- [ ] System prompt creates appropriate Harada-style plans
- [ ] Response parsing validates JSON structure
- [ ] Error handling for API failures implemented
- [ ] Function tested with multiple example goals
- [ ] Returns well-structured plans with 2-4 sub-goals and 3-6 action steps each

---

## Story 2.3: Build Goal Creation API Endpoint

**As a** logged-in user,
**I want** to submit my goal description and receive a personalized plan,
**so that** I can start working toward my goal with structured guidance.

### Acceptance Criteria

1. `POST /api/goals` endpoint requires authentication (valid JWT token), accepts request body: `{ title, description }`
2. Endpoint calls `generateGoalPlan` service with goal description to get AI-generated plan structure
3. Endpoint creates Goal record in database with title, description, and links to authenticated user
4. For each sub-goal in AI response, create SubGoal record linked to Goal with proper order
5. For each action step in AI response, create ActionStep record linked to SubGoal with proper order, status defaulting to "pending"
6. Endpoint returns complete goal structure as JSON including all sub-goals and action steps with IDs
7. Error handling returns 400 if title/description missing, 500 if Gemini API fails, 401 if not authenticated
8. Endpoint respects Gemini rate limiting (if 1500 requests/day quota approaching, return 429 Too Many Requests)

### Technical Notes

- **Framework:** FastAPI with Pydantic models
- **Authentication:** JWT token validation via dependency injection
- **Rate Limiting:** slowapi 0.1.9 for per-user quotas
- **Transaction:** Wrap goal creation in database transaction (rollback on failure)

### API Endpoint Specification

**POST /api/goals**

Request:
```json
{
  "title": "Learn Python Programming",
  "description": "I want to learn Python to build web applications and automate tasks. I'm a complete beginner with no programming experience."
}
```

Response (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Learn Python Programming",
  "description": "I want to learn Python...",
  "status": "active",
  "created_at": "2025-12-14T10:00:00Z",
  "updated_at": "2025-12-14T10:00:00Z",
  "sub_goals": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "title": "Master Python Basics",
      "order": 1,
      "action_steps": [
        {
          "id": "770e8400-e29b-41d4-a716-446655440002",
          "title": "Install Python and set up development environment",
          "description": "Download Python 3.11+ from python.org, install VS Code, and configure Python extension",
          "status": "pending",
          "order": 1,
          "estimated_minutes": 20
        }
      ]
    }
  ]
}
```

### Pydantic Schemas

```python
class GoalCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)

class ActionStepResponse(BaseModel):
    id: UUID
    title: str
    description: str
    status: str
    order: int
    estimated_minutes: int

class SubGoalResponse(BaseModel):
    id: UUID
    title: str
    order: int
    action_steps: List[ActionStepResponse]

class GoalResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    sub_goals: List[SubGoalResponse]
```

### Definition of Done

- [ ] POST /api/goals endpoint implemented with authentication
- [ ] Endpoint calls generateGoalPlan service
- [ ] Goal, SubGoal, and ActionStep records created in database
- [ ] Complete goal structure returned in response
- [ ] Error handling for validation, API failures, and auth issues
- [ ] Rate limiting implemented to protect Gemini quota
- [ ] Endpoint tested with valid and invalid inputs

---

## Story 2.4: Create Goal Input and Display UI

**As a** logged-in user,
**I want** a form to describe my goal and see the AI-generated plan,
**so that** I can easily create and visualize my personalized roadmap.

### Acceptance Criteria

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

### Technical Notes

- **Form Handling:** React Hook Form 7.51.0 with Zod validation
- **Routing:** Next.js 14 App Router with dynamic routes
- **Styling:** Tailwind CSS with responsive design
- **State Management:** React useState for form state, useRouter for navigation

### UI Components

**Goal Creation Form (`/goals/new`)**
- Title input (max 100 chars with character counter)
- Description textarea (max 500 chars with character counter)
- "Generate My Plan" button (loading state during API call)
- Error message display area

**Goal Detail View (`/goals/[goalId]`)**
- Goal header (title, description)
- Sub-goal cards (expandable/collapsible)
- Action step list with checkboxes and time estimates
- Back to dashboard link

### Form Validation

```typescript
const goalSchema = z.object({
  title: z.string()
    .min(1, "Title is required")
    .max(100, "Title must be 100 characters or less"),
  description: z.string()
    .min(1, "Description is required")
    .max(500, "Description must be 500 characters or less")
});
```

### Definition of Done

- [ ] Dashboard has "+ Create New Goal" button
- [ ] Goal creation form functional with validation
- [ ] Form shows loading state during API call
- [ ] Successful creation redirects to goal detail page
- [ ] Goal detail page displays full plan structure
- [ ] Sub-goals are expandable/collapsible
- [ ] Action steps display with checkboxes and time estimates
- [ ] Error messages display appropriately
- [ ] Responsive design works on mobile and desktop

---

## Story 2.5: Implement Goal Editing and Deletion

**As a** logged-in user,
**I want** to modify my goal plan if the AI-generated steps aren't quite right,
**so that** I can customize the plan to fit my actual situation and capabilities.

### Acceptance Criteria

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

### Technical Notes

- **Authorization:** Verify goal/action step belongs to authenticated user
- **Optimistic UI:** Update UI immediately, rollback on API failure
- **Confirmation Dialog:** Use Radix UI Dialog for accessible modal

### API Endpoints

**PATCH /api/goals/:goalId**
```json
Request:
{
  "title": "Updated Goal Title",
  "description": "Updated description"
}

Response (200 OK):
{
  "id": "goal-uuid",
  "title": "Updated Goal Title",
  "description": "Updated description",
  "updated_at": "2025-12-14T11:00:00Z"
}
```

**DELETE /api/goals/:goalId**
```
Response (204 No Content)
```

**PATCH /api/action-steps/:stepId**
```json
Request:
{
  "title": "Updated step title",
  "description": "Updated description",
  "estimated_minutes": 25
}

Response (200 OK):
{
  "id": "step-uuid",
  "title": "Updated step title",
  "description": "Updated description",
  "estimated_minutes": 25,
  "updated_at": "2025-12-14T11:00:00Z"
}
```

**DELETE /api/action-steps/:stepId**
```
Response (204 No Content)
```

### UI Enhancements

- "Edit Goal" button on goal detail page
- Inline edit mode or modal for goal title/description
- "Delete Goal" button with confirmation dialog
- "Edit" icon on each action step for inline editing
- "Delete" icon on each action step
- Optimistic UI updates with error rollback

### Definition of Done

- [ ] PATCH and DELETE endpoints for goals implemented
- [ ] PATCH and DELETE endpoints for action steps implemented
- [ ] Authorization checks prevent unauthorized edits
- [ ] Goal detail page has edit and delete functionality
- [ ] Action steps can be edited and deleted inline
- [ ] Confirmation dialog for goal deletion
- [ ] Optimistic UI updates with error handling
- [ ] Dashboard shows list of all user's active goals
- [ ] Changes persist correctly to database

---

## Story 2.6: Add Goal List and Dashboard Overview

**As a** logged-in user,
**I want** to see all my active goals on the dashboard,
**so that** I can quickly access any goal and track my overall progress.

### Acceptance Criteria

1. `GET /api/goals` endpoint returns all goals for authenticated user with basic info (id, title, status, progress percentage calculated as completed steps / total steps)
2. Dashboard displays goal cards in grid layout (responsive: 1 column mobile, 2-3 columns desktop)
3. Each goal card shows goal title, progress bar (0-100%), and "View Details" button linking to `/goals/[goalId]`
4. If user has no goals, dashboard shows empty state with "+ Create Your First Goal" button
5. Dashboard shows placeholder for future features: "🔥 Current Streak: 0 days" (not functional yet, coming in Epic 3)
6. Goal cards use distinct visual styling (border, shadow, hover effect) to feel interactive
7. Goals are sorted by createdAt descending (newest goals first)
8. Clicking anywhere on goal card (not just button) navigates to goal detail page

### Technical Notes

- **Progress Calculation:** (completed action steps / total action steps) * 100
- **Grid Layout:** Tailwind CSS grid utilities (grid-cols-1 md:grid-cols-2 lg:grid-cols-3)
- **Empty State:** Centered message with prominent CTA button

### API Endpoint

**GET /api/goals**
```json
Response (200 OK):
[
  {
    "id": "goal-uuid-1",
    "title": "Learn Python Programming",
    "status": "active",
    "progress": 25.5,
    "created_at": "2025-12-14T10:00:00Z"
  },
  {
    "id": "goal-uuid-2",
    "title": "Get Fit",
    "status": "active",
    "progress": 60.0,
    "created_at": "2025-12-13T09:00:00Z"
  }
]
```

### Dashboard Layout

```
┌─────────────────────────────────────────┐
│  Welcome, user@example.com!             │
│  🔥 Current Streak: 0 days (placeholder)│
├─────────────────────────────────────────┤
│  Your Goals                             │
│  [+ Create New Goal]                    │
├─────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌────────┐│
│  │ Goal 1   │  │ Goal 2   │  │ Goal 3 ││
│  │ [====  ] │  │ [======] │  │ [==   ]││
│  │ 25%      │  │ 60%      │  │ 15%    ││
│  └──────────┘  └──────────┘  └────────┘│
└─────────────────────────────────────────┘
```

### Goal Card Component

- Goal title (truncate if too long)
- Progress bar (visual representation of completion %)
- Progress percentage text
- Hover effect (scale, shadow, border color change)
- Click anywhere to navigate to goal detail

### Definition of Done

- [ ] GET /api/goals endpoint returns goals with progress
- [ ] Dashboard displays goal cards in responsive grid
- [ ] Goal cards show title, progress bar, and percentage
- [ ] Empty state displays for users with no goals
- [ ] Placeholder for streak counter visible
- [ ] Goals sorted by creation date (newest first)
- [ ] Clicking goal card navigates to goal detail page
- [ ] Responsive design works on mobile and desktop

---

## Epic 2 Summary

### Stories Completed
- 6 stories total
- All P0 (must-have) stories

### Key Deliverables
1. ✅ Database schema for goals, sub-goals, and action steps
2. ✅ Gemini API integration for AI-powered goal planning
3. ✅ Goal creation API with structured plan generation
4. ✅ Goal input and display UI
5. ✅ Goal editing and deletion functionality
6. ✅ Dashboard with goal list and progress tracking

### Core Features Implemented
- AI-powered goal plan generation using Gemini 1.5 Flash
- Harada-style structured plans (2-4 sub-goals, 3-6 action steps per sub-goal)
- Full CRUD operations for goals and action steps
- Visual progress tracking (percentage completion)
- Responsive UI with Tailwind CSS
- Authorization and data validation

### Technical Achievements
- Gemini API integration with error handling and rate limiting
- Structured JSON parsing and validation
- Database relationships with cascade delete
- Optimistic UI updates
- RESTful API design with Pydantic schemas

### What's Next
With Epic 2 complete, users can create and manage AI-generated goal plans. Epic 3 will implement the unique Socratic Mentor AI system and progress tracking with streaks.

**Ready for Epic 3: Socratic Mentor AI & Progress Tracking** 🚀
