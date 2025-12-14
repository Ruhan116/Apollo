# Epic 3: Socratic Mentor AI & Progress Tracking

**Project:** Apollo
**Epic Goal:** Implement the dual AI system (Socratic Mentor AI + Emotional Support AI) with chat interface, intelligent context switching based on user emotion/progress, and streak-based progress tracking. This delivers Apollo's unique value proposition: an AI that guides users to find answers themselves rather than giving direct solutions, combined with habit-forming streak mechanics.

**Priority:** P0 (Must Have)
**Estimated Timeline:** Days 11-16 of development
**Dependencies:** Epic 2 (AI-Powered Goal Planning)

---

## Story 3.1: Extend Database Schema for Progress and Chat

**As a** developer,
**I want** database models for tracking action step completion, streaks, and AI chat conversations,
**so that** we can persist user progress and conversation history.

### Acceptance Criteria

1. SQLAlchemy `User` model updated with additional fields: current_streak (Integer, default 0), longest_streak (Integer, default 0), last_active_date (DateTime, nullable)
2. SQLAlchemy `ActionStep` model adds field: completed_at (DateTime, nullable) to track when step was completed
3. SQLAlchemy model defines `ChatMessage` class with fields: id, user_id, goal_id (nullable, ForeignKey), action_step_id (nullable, ForeignKey), role (enum: user, mentor, emotional_support), content (Text), timestamp (DateTime)
4. SQLAlchemy model defines `UserProgress` class with fields: id, user_id (ForeignKey), date (Date, unique constraint with user_id), actions_completed (Integer), minutes_worked (Integer)
5. Alembic migration created for schema changes (`alembic revision --autogenerate -m "Add progress tracking and chat"`)
6. Migration applied to Azure PostgreSQL (`alembic upgrade head`)
7. Can create chat messages and update progress via SQLAlchemy session (verified with test script or pytest)

### Technical Notes

- **New Models:** ChatMessage, UserProgress
- **Updated Models:** User (streak fields), ActionStep (completed_at)
- **Unique Constraint:** UserProgress has unique constraint on (user_id, date) to prevent duplicate daily records

### Database Schema Extensions

**User Model Updates**
```python
class User(Base):
    # ... existing fields ...
    current_streak = Column(Integer, default=0, nullable=False)
    longest_streak = Column(Integer, default=0, nullable=False)
    last_active_date = Column(Date, nullable=True)
```

**ActionStep Model Updates**
```python
class ActionStep(Base):
    # ... existing fields ...
    completed_at = Column(DateTime, nullable=True)
```

**ChatMessage Model**
```python
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="CASCADE"), nullable=True, index=True)
    action_step_id = Column(UUID(as_uuid=True), ForeignKey("action_steps.id", ondelete="CASCADE"), nullable=True, index=True)
    role = Column(Enum("user", "mentor", "emotional_support", name="chat_role"), nullable=False)
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="chat_messages")
    goal = relationship("Goal", back_populates="chat_messages")
    action_step = relationship("ActionStep", back_populates="chat_messages")
```

**UserProgress Model**
```python
class UserProgress(Base):
    __tablename__ = "user_progress"
    __table_args__ = (
        UniqueConstraint('user_id', 'date', name='uix_user_date'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    actions_completed = Column(Integer, default=0, nullable=False)
    minutes_worked = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="progress_records")
```

### Definition of Done

- [ ] User model updated with streak tracking fields
- [ ] ActionStep model has completed_at field
- [ ] ChatMessage model created with role enum
- [ ] UserProgress model created with unique constraint
- [ ] Alembic migration created and applied
- [ ] Models tested with CRUD operations
- [ ] Relationships configured correctly

---

## Story 3.2: Build Socratic Mentor AI Service

**As a** developer,
**I want** a backend service that implements Socratic questioning using Gemini,
**so that** the AI guides users without giving direct answers.

### Acceptance Criteria

1. `socraticMentor` service function accepts user message, conversation history, and current goal/action step context
2. System prompt instructs Gemini to act as Socratic mentor: ask guiding questions, never provide direct answers/solutions/code, help user think through problems themselves
3. System prompt includes explicit examples of Socratic responses vs. prohibited direct answers (e.g., "What have you tried so far?" vs. "Here's the solution: ...")
4. System prompt includes user's current action step context to keep questions relevant
5. Function calls Gemini 1.5 Flash API with conversation history (last 10 messages max to control token usage)
6. Response is validated to ensure it doesn't contain direct answers (basic keyword detection: no code blocks, no step-by-step solutions) - if detected, re-prompt with stronger Socratic enforcement
7. Function returns Gemini response and logs conversation to database (ChatMessage with role: mentor)
8. Manually tested with 10 scenarios (user asking "how do I...", "what is...", etc.) and confirms AI asks questions back at least 70% of the time

### Technical Notes

- **AI Model:** Gemini 1.5 Flash
- **Conversation History:** Last 10 messages to control token usage
- **Validation:** Basic keyword detection for direct answers
- **Retry Logic:** Re-prompt if direct answer detected

### System Prompt

```python
SOCRATIC_MENTOR_PROMPT = """You are a Socratic mentor helping a learner achieve their goals.

Your role is to guide through questions, NOT provide direct answers or solutions.

Core Principles:
1. Ask thought-provoking questions that help the user think through the problem
2. NEVER provide direct answers, step-by-step instructions, code snippets, or solutions
3. Help users discover answers themselves through guided inquiry
4. Be patient, encouraging, and non-judgmental
5. Reference the user's current action step to keep guidance focused

Current Action Step: {action_step_title}
Description: {action_step_description}

Examples of GOOD Socratic responses:
- "What have you tried so far?"
- "What do you think might be causing that issue?"
- "How would you break this problem down into smaller parts?"
- "What resources have you considered exploring?"
- "What's your understanding of this concept right now?"

Examples of PROHIBITED responses:
- "Here's how to do it: [step-by-step instructions]"
- "The answer is X because Y"
- "Try this code: [code block]"
- "You need to do A, then B, then C"

Remember: Your job is to guide discovery, not provide answers. Ask questions that help the user think critically and learn through their own reasoning.

Conversation so far:
{conversation_history}

User's latest message: {user_message}

Your Socratic response:"""
```

### Service Function Signature

```python
async def socraticMentor(
    user_message: str,
    user_id: UUID,
    goal_id: UUID,
    action_step_id: Optional[UUID] = None,
    conversation_history: List[ChatMessage] = []
) -> str:
    """
    Generate a Socratic mentoring response using Gemini API.

    Args:
        user_message: User's latest message
        user_id: User ID for logging
        goal_id: Current goal context
        action_step_id: Optional action step context
        conversation_history: Recent chat messages (last 10)

    Returns:
        Socratic mentor response string

    Raises:
        GeminiAPIError: If API call fails
    """
```

### Validation Logic

```python
def validate_socratic_response(response: str) -> bool:
    """
    Check if response contains prohibited direct answers.

    Returns True if response is Socratic, False if it contains direct answers.
    """
    prohibited_patterns = [
        r'```',  # Code blocks
        r'here\'s how',  # Direct instructions
        r'the answer is',  # Direct answers
        r'step 1:|step 2:|step 3:',  # Step-by-step solutions
    ]

    for pattern in prohibited_patterns:
        if re.search(pattern, response, re.IGNORECASE):
            return False
    return True
```

### Definition of Done

- [ ] socraticMentor service function implemented
- [ ] System prompt emphasizes Socratic questioning
- [ ] Function calls Gemini API with conversation history
- [ ] Response validation detects direct answers
- [ ] Re-prompting logic implemented for invalid responses
- [ ] Chat messages logged to database
- [ ] Manually tested with 10 scenarios (70%+ Socratic success rate)
- [ ] Error handling for API failures

---

## Story 3.3: Build Emotional Support AI Service

**As a** developer,
**I want** a backend service that detects user frustration and provides encouragement,
**so that** users feel supported when genuinely stuck.

### Acceptance Criteria

1. `emotionalSupport` service function accepts user message and recent progress history (action steps completed in last 7 days)
2. System prompt instructs Gemini to act as empathetic coach: validate feelings, provide encouragement, suggest taking breaks or switching tasks if user seems overwhelmed
3. `detectFrustration` helper function analyzes user message for frustration signals using Gemini: asks "Is the user expressing frustration, confusion, or feeling stuck? Answer: Yes/No/Unsure" and parses response
4. Frustration detection considers progress history: if user hasn't completed steps in 3+ days AND message contains negative language, likely frustrated
5. When frustration detected, function triggers emotional support mode and offers encouragement with specific acknowledgment of their struggle
6. Function returns supportive response and logs to database (ChatMessage with role: emotional_support)
7. Manually tested with 5 frustrated user messages (e.g., "I don't understand this", "This is too hard", "I've been stuck for days") and confirms empathetic responses

### Technical Notes

- **AI Model:** Gemini 1.5 Flash
- **Frustration Detection:** Sentiment analysis + progress history
- **Multi-Signal Detection:** Message content + behavioral patterns

### System Prompts

**Frustration Detection Prompt**
```python
FRUSTRATION_DETECTION_PROMPT = """Analyze the following user message for signs of frustration, confusion, or feeling stuck.

User's message: "{user_message}"

Recent progress context:
- Last action completed: {days_since_last_completion} days ago
- Total actions completed in last 7 days: {recent_completions}

Answer with ONLY one word: Yes, No, or Unsure

Is the user expressing frustration, confusion, or feeling stuck?"""
```

**Emotional Support Prompt**
```python
EMOTIONAL_SUPPORT_PROMPT = """You are an empathetic learning coach providing emotional support.

The user is feeling frustrated or stuck with their learning journey. Your role is to:
1. Validate their feelings without judgment
2. Provide genuine encouragement
3. Suggest constructive next steps (taking a break, switching tasks, asking for help)
4. Remind them that struggle is normal and part of the learning process

Current Action Step: {action_step_title}
User's frustration: {user_message}

Progress context:
- Days since last completion: {days_since_last_completion}
- Recent actions completed: {recent_completions}

Provide a warm, empathetic response that acknowledges their struggle and offers supportive guidance.

Your response:"""
```

### Service Function Signatures

```python
async def detectFrustration(
    user_message: str,
    user_id: UUID,
    recent_progress: UserProgress
) -> dict:
    """
    Detect if user is frustrated based on message and progress.

    Returns:
        {
            "is_frustrated": bool,
            "confidence": "high" | "medium" | "low",
            "reason": str
        }
    """

async def emotionalSupport(
    user_message: str,
    user_id: UUID,
    goal_id: UUID,
    action_step_id: Optional[UUID] = None,
    recent_progress: UserProgress = None
) -> str:
    """
    Generate empathetic support response using Gemini API.

    Returns:
        Emotional support response string
    """
```

### Detection Logic

```python
def analyze_progress_patterns(recent_progress: UserProgress) -> dict:
    """
    Analyze user's recent progress for stuck indicators.

    Returns:
        {
            "days_since_last_completion": int,
            "recent_completions": int,
            "is_stalled": bool
        }
    """
    today = datetime.now().date()
    last_completion = recent_progress.date if recent_progress else None

    if last_completion:
        days_since = (today - last_completion).days
    else:
        days_since = 999  # No completions

    return {
        "days_since_last_completion": days_since,
        "recent_completions": recent_progress.actions_completed if recent_progress else 0,
        "is_stalled": days_since >= 3
    }
```

### Definition of Done

- [ ] emotionalSupport service function implemented
- [ ] detectFrustration helper function implemented
- [ ] System prompts provide empathetic responses
- [ ] Frustration detection uses message + progress signals
- [ ] Function logs emotional support messages to database
- [ ] Manually tested with 5 frustrated messages (empathetic responses)
- [ ] Error handling for API failures

---

## Story 3.4: Implement AI Chat API Endpoint with Context Switching

**As a** logged-in user,
**I want** to chat with the AI mentor about my current action step,
**so that** I can get guidance when I'm unsure how to proceed.

### Acceptance Criteria

1. `POST /api/chat` endpoint requires authentication, accepts request body: `{ message, goalId, actionStepId (optional) }`
2. Endpoint retrieves conversation history (last 10 ChatMessages for this user + goal)
3. Endpoint calls `detectFrustration` function to determine user emotional state
4. If frustration detected AND user hasn't completed steps recently, call `emotionalSupport` service
5. Otherwise, call `socraticMentor` service with goal/action step context
6. Response includes: `{ reply, aiMode: 'mentor' | 'emotional_support' }` so frontend can differentiate
7. Endpoint saves both user message and AI response to ChatMessage table
8. Error handling catches Gemini API failures and returns fallback message: "I'm having trouble connecting right now. Please try again in a moment."
9. Endpoint respects rate limiting (max 20 messages per user per day for MVP to stay within Gemini quota)

### Technical Notes

- **Framework:** FastAPI with async endpoints
- **Rate Limiting:** slowapi with per-user limits (20 messages/day)
- **Context Switching:** Automatic based on frustration detection
- **Transaction:** Save both user and AI messages in single transaction

### API Endpoint Specification

**POST /api/chat**

Request:
```json
{
  "message": "I don't understand how to install Python",
  "goal_id": "550e8400-e29b-41d4-a716-446655440000",
  "action_step_id": "770e8400-e29b-41d4-a716-446655440002"
}
```

Response (200 OK):
```json
{
  "reply": "It sounds like you're feeling stuck with the installation process. That's completely normal - setting up development environments can be confusing at first. What specific part is giving you trouble?",
  "ai_mode": "emotional_support",
  "message_id": "880e8400-e29b-41d4-a716-446655440003",
  "timestamp": "2025-12-14T10:30:00Z"
}
```

### Endpoint Implementation

```python
@router.post("/chat", response_model=ChatResponse)
@limiter.limit("20/day")
async def chat_with_mentor(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Chat with AI mentor (Socratic or Emotional Support mode).

    Automatically switches between modes based on user state.
    """
    # 1. Retrieve conversation history
    history = await get_conversation_history(
        db, current_user.id, request.goal_id, limit=10
    )

    # 2. Get recent progress
    recent_progress = await get_recent_progress(db, current_user.id, days=7)

    # 3. Detect frustration
    frustration = await detectFrustration(
        request.message, current_user.id, recent_progress
    )

    # 4. Choose AI mode
    if frustration["is_frustrated"] and frustration["confidence"] == "high":
        ai_mode = "emotional_support"
        reply = await emotionalSupport(
            request.message, current_user.id, request.goal_id,
            request.action_step_id, recent_progress
        )
    else:
        ai_mode = "mentor"
        reply = await socraticMentor(
            request.message, current_user.id, request.goal_id,
            request.action_step_id, history
        )

    # 5. Save messages to database
    await save_chat_messages(db, current_user.id, request, reply, ai_mode)

    return ChatResponse(reply=reply, ai_mode=ai_mode)
```

### Pydantic Schemas

```python
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    goal_id: UUID
    action_step_id: Optional[UUID] = None

class ChatResponse(BaseModel):
    reply: str
    ai_mode: Literal["mentor", "emotional_support"]
    message_id: UUID
    timestamp: datetime
```

### Definition of Done

- [ ] POST /api/chat endpoint implemented with authentication
- [ ] Endpoint retrieves conversation history
- [ ] Frustration detection integrated into endpoint
- [ ] Context switching between mentor/emotional support modes
- [ ] Both user and AI messages saved to database
- [ ] Error handling with fallback messages
- [ ] Rate limiting (20 messages/day per user)
- [ ] Endpoint tested with various message types

---

## Story 3.5: Build AI Chat Interface UI

**As a** logged-in user,
**I want** a chat interface on my goal page where I can ask questions about my action steps,
**so that** I can get Socratic guidance when I'm unsure how to proceed.

### Acceptance Criteria

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

### Technical Notes

- **Real-time Updates:** Optimistic UI (add message immediately, rollback on error)
- **Auto-scroll:** Scroll to bottom when new messages arrive
- **Context Display:** Show currently selected action step above chat
- **Keyboard Shortcuts:** Enter to send, Shift+Enter for new line

### Chat Interface Components

**Chat Container**
- Collapsible section (collapsed by default)
- Message list (scrollable, auto-scroll to bottom)
- Input area (textarea + send button)
- Context display (current action step)

**Message Bubble**
- User message: right-aligned, blue background
- AI mentor: left-aligned, gray background, "🤔 Mentor" badge
- AI support: left-aligned, green background, "💙 Support" badge
- Timestamp (small, gray text)

**Input Area**
- Textarea (auto-resize, max 5 lines)
- Send button (disabled when empty or during API call)
- Loading indicator ("Sending...")
- Character counter (0/1000)

### Chat UI Layout

```
┌─────────────────────────────────────────┐
│ Currently working on: Install Python    │
├─────────────────────────────────────────┤
│  🤔 Mentor                              │
│  Hello! I'm here to help you think     │
│  through this step. What questions do   │
│  you have about installing Python?      │
│                                         │
│                      I don't know where│
│                      to start :(       │
│                                         │
│  💙 Support                             │
│  That's completely normal! Many people  │
│  feel uncertain at the beginning...     │
├─────────────────────────────────────────┤
│  [Type your message here...     ] [Send]│
└─────────────────────────────────────────┘
```

### Action Step Selection

- Action steps in goal view have hover effect
- Clicking action step highlights it and updates chat context
- Selected step shown above chat: "Currently working on: [title]"
- Unselect by clicking again or clicking different step

### Definition of Done

- [ ] Chat interface added to goal detail page
- [ ] Messages display with correct alignment and colors
- [ ] AI mode badges (Mentor/Support) displayed
- [ ] Chat input supports Enter to send, Shift+Enter for new line
- [ ] Optimistic UI updates with error rollback
- [ ] Auto-scroll to bottom on new messages
- [ ] Action step selection updates chat context
- [ ] Conversation history loads on page mount
- [ ] Mobile responsive design
- [ ] Loading states during API calls

---

## Story 3.6: Implement Action Step Completion and Streak Tracking

**As a** logged-in user,
**I want** to mark action steps as complete and see my daily streak,
**so that** I feel motivated to work on my goals consistently.

### Acceptance Criteria

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

### Technical Notes

- **Streak Logic:** lastActiveDate tracking with gap detection
- **Progress Aggregation:** Daily UserProgress records
- **Atomic Updates:** Use database transaction for step completion + progress update
- **Celebration:** Toast notification library (react-hot-toast)

### API Endpoints

**POST /api/action-steps/:stepId/complete**

Response (200 OK):
```json
{
  "action_step": {
    "id": "step-uuid",
    "status": "completed",
    "completed_at": "2025-12-14T10:45:00Z"
  },
  "user_progress": {
    "current_streak": 3,
    "longest_streak": 5,
    "actions_today": 2,
    "minutes_today": 45
  }
}
```

**POST /api/action-steps/:stepId/uncomplete**

Response (200 OK):
```json
{
  "action_step": {
    "id": "step-uuid",
    "status": "pending",
    "completed_at": null
  },
  "user_progress": {
    "current_streak": 3,
    "actions_today": 1,
    "minutes_today": 25
  }
}
```

### Streak Calculation Logic

```python
def calculate_streak(user: User, today: date) -> dict:
    """
    Calculate streak based on last active date.

    Returns:
        {
            "current_streak": int,
            "longest_streak": int,
            "updated": bool
        }
    """
    if user.last_active_date is None:
        # First activity ever
        return {"current_streak": 1, "longest_streak": 1, "updated": True}

    gap_days = (today - user.last_active_date).days

    if gap_days == 0:
        # Same day, no change
        return {"current_streak": user.current_streak, "longest_streak": user.longest_streak, "updated": False}
    elif gap_days == 1:
        # Consecutive day, increment streak
        new_streak = user.current_streak + 1
        new_longest = max(new_streak, user.longest_streak)
        return {"current_streak": new_streak, "longest_streak": new_longest, "updated": True}
    else:
        # Gap > 1 day, reset streak
        new_longest = max(user.current_streak, user.longest_streak)
        return {"current_streak": 1, "longest_streak": new_longest, "updated": True}
```

### Completion Endpoint Implementation

```python
@router.post("/action-steps/{step_id}/complete")
async def complete_action_step(
    step_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    async with db.begin():
        # 1. Get and validate action step
        step = await get_action_step(db, step_id, current_user.id)

        # 2. Mark as completed
        step.status = "completed"
        step.completed_at = datetime.utcnow()

        # 3. Update user progress for today
        today = date.today()
        progress = await get_or_create_progress(db, current_user.id, today)
        progress.actions_completed += 1
        progress.minutes_worked += step.estimated_minutes

        # 4. Update streak
        streak = calculate_streak(current_user, today)
        if streak["updated"]:
            current_user.current_streak = streak["current_streak"]
            current_user.longest_streak = streak["longest_streak"]
            current_user.last_active_date = today

        await db.commit()

        return {
            "action_step": step,
            "user_progress": {
                "current_streak": current_user.current_streak,
                "longest_streak": current_user.longest_streak,
                "actions_today": progress.actions_completed,
                "minutes_today": progress.minutes_worked
            }
        }
```

### UI Enhancements

**Dashboard Streak Display**
```tsx
<div className="streak-card">
  <div className="streak-icon">🔥</div>
  <div className="streak-count">{currentStreak} days</div>
  <div className="streak-label">Current Streak</div>
  <div className="streak-best">Best: {longestStreak} days</div>
</div>
```

**Action Step Checkbox**
- Interactive checkbox (controlled component)
- Click triggers API call
- Optimistic UI update (check immediately, rollback on error)
- Strikethrough text for completed steps
- Toast notification on completion

### Definition of Done

- [ ] Complete/uncomplete endpoints implemented
- [ ] UserProgress records updated on completion
- [ ] Streak calculation logic working correctly
- [ ] Action step checkboxes functional
- [ ] Dashboard displays current streak prominently
- [ ] Dashboard shows actions completed today
- [ ] Celebration toast on action completion
- [ ] Optimistic UI updates with error handling
- [ ] Streak persists across sessions

---

## Story 3.7: Add Daily Check-In Prompt

**As a** logged-in user,
**I want** a daily check-in prompt when I log in,
**so that** I'm encouraged to choose what to work on and stay focused.

### Acceptance Criteria

1. When user loads dashboard, check if they've completed any actions today (query UserProgress for today's date)
2. If no actions completed today AND user has active goals, show modal/banner: "What are you working on today?"
3. Modal lists user's active goals with next incomplete action step for each goal
4. User can click an action step to navigate to that goal's detail page with the action step pre-selected
5. Modal includes "I'll decide later" button to dismiss without selecting
6. Check-in modal only appears once per day (track in localStorage or session storage that user saw it)
7. If user has no active goals, check-in shows: "Ready to start? Create your first goal!" with link to goal creation page
8. Check-in is non-blocking (user can close it and still access dashboard normally)

### Technical Notes

- **Modal Library:** Radix UI Dialog for accessibility
- **Persistence:** localStorage to track "seen today" flag
- **Navigation:** Next.js router with query params for pre-selected step

### Daily Check-In Modal

**Modal Trigger Logic**
```typescript
useEffect(() => {
  const checkInKey = `check-in-${format(new Date(), 'yyyy-MM-dd')}`;
  const hasSeenToday = localStorage.getItem(checkInKey);

  if (!hasSeenToday && actionsToday === 0 && activeGoals.length > 0) {
    setShowCheckIn(true);
  }
}, [actionsToday, activeGoals]);

const dismissCheckIn = () => {
  const checkInKey = `check-in-${format(new Date(), 'yyyy-MM-dd')}`;
  localStorage.setItem(checkInKey, 'true');
  setShowCheckIn(false);
};
```

**Modal Content**

```
┌─────────────────────────────────────────┐
│  What are you working on today?         │
├─────────────────────────────────────────┤
│  Goal: Learn Python Programming         │
│    → Install Python (20 min)            │
│    → Write first Hello World (10 min)   │
│                                         │
│  Goal: Get Fit                          │
│    → 10-minute walk (10 min)            │
├─────────────────────────────────────────┤
│  [I'll decide later]                    │
└─────────────────────────────────────────┘
```

**Goal Selection**
- Each goal shows title
- Next incomplete action step displayed with time estimate
- Click action step → navigate to goal detail with step pre-selected
- Pre-selection via URL query param: `/goals/[id]?step=[stepId]`

**Empty State (No Goals)**
```
┌─────────────────────────────────────────┐
│  Ready to start?                        │
│                                         │
│  Create your first goal to get          │
│  personalized guidance!                 │
│                                         │
│  [+ Create Your First Goal]             │
└─────────────────────────────────────────┘
```

### Definition of Done

- [ ] Check-in modal triggers on dashboard load
- [ ] Modal only shows if no actions completed today
- [ ] Lists active goals with next action steps
- [ ] Clicking action step navigates to goal detail
- [ ] "I'll decide later" button dismisses modal
- [ ] Modal only appears once per day (localStorage)
- [ ] Empty state for users with no goals
- [ ] Non-blocking (can close and use dashboard)
- [ ] Mobile responsive design

---

## Epic 3 Summary

### Stories Completed
- 7 stories total
- All P0 (must-have) stories

### Key Deliverables
1. ✅ Extended database schema for progress tracking and chat
2. ✅ Socratic Mentor AI service (guides without giving answers)
3. ✅ Emotional Support AI service (detects frustration, provides encouragement)
4. ✅ AI chat API with intelligent context switching
5. ✅ Chat interface UI with conversation history
6. ✅ Action step completion with streak tracking
7. ✅ Daily check-in prompt for focus and motivation

### Core Features Implemented
- **Dual AI System:** Socratic Mentor + Emotional Support with automatic switching
- **Frustration Detection:** Multi-signal analysis (message sentiment + progress patterns)
- **Streak Mechanics:** Daily streak tracking with celebration UI
- **Progress Tracking:** UserProgress records with daily aggregation
- **Chat Interface:** Conversational UI with context-aware guidance
- **Daily Check-In:** Focus prompt to encourage consistent engagement

### Technical Achievements
- Gemini API integration for dual AI personas
- Context switching based on user emotional state
- Socratic response validation (70%+ question-based responses)
- Atomic transactions for progress updates
- Real-time chat with optimistic UI
- Streak calculation with gap detection

### What's Next
With Epic 3 complete, Apollo has its core differentiator: an AI that teaches rather than tells. Epic 4 (optional) will add dynamic micro-stepping for adaptive scaffolding when users are genuinely stuck.

**Ready for Epic 4: Dynamic Micro-Stepping & Adaptive Scaffolding (P1 - OPTIONAL)** 🚀
