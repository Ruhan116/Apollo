# Epic 4: Dynamic Micro-Stepping & Adaptive Scaffolding

**Project:** Apollo
**Epic Goal:** Build the intelligent system that detects when users are genuinely stuck (not lazy) and automatically breaks down overwhelming action steps into 5-10 minute micro-steps. This demonstrates Apollo's adaptive scaffolding capability - preserving user agency and learning while removing unproductive friction.

**Priority:** P1 (Nice-to-Have - OPTIONAL)
**Estimated Timeline:** Days 17-20 of development (if schedule allows)
**Dependencies:** Epic 3 (Socratic Mentor AI & Progress Tracking)

**⚠️ NOTE:** This epic is P1 (nice-to-have). **Cut if behind schedule by Dec 23.** Epics 1-3 deliver the core Apollo value proposition.

---

## Story 4.1: Extend Database Schema for Micro-Steps

**As a** developer,
**I want** database models for storing micro-steps and stuck detection metadata,
**so that** we can track when scaffolding is offered and how users engage with it.

### Acceptance Criteria

1. SQLAlchemy model defines `MicroStep` class with fields: id, action_step_id (ForeignKey), title, order (Integer), status (enum: pending, completed), completed_at (DateTime, nullable), created_at (DateTime)
2. SQLAlchemy `ActionStep` model adds fields: micro_steps_generated (Boolean, default False), stuck_detected_at (DateTime, nullable), micro_step_exited_at (DateTime, nullable)
3. SQLAlchemy `ChatMessage` model adds field: triggered_micro_stepping (Boolean, default False) to track when conversation led to scaffolding
4. Alembic migration created and applied (`alembic revision --autogenerate` then `alembic upgrade head`)
5. Can create micro-steps and update action step flags via SQLAlchemy session

### Technical Notes

- **New Model:** MicroStep
- **Updated Models:** ActionStep (scaffolding metadata), ChatMessage (trigger tracking)
- **Cascade Delete:** MicroSteps deleted when parent ActionStep is deleted

### Database Schema

**MicroStep Model**
```python
class MicroStep(Base):
    __tablename__ = "micro_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    action_step_id = Column(UUID(as_uuid=True), ForeignKey("action_steps.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    order = Column(Integer, nullable=False)
    status = Column(Enum("pending", "completed", name="micro_step_status"), default="pending", nullable=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    action_step = relationship("ActionStep", back_populates="micro_steps")
```

**ActionStep Model Updates**
```python
class ActionStep(Base):
    # ... existing fields ...

    # Micro-stepping metadata
    micro_steps_generated = Column(Boolean, default=False, nullable=False)
    stuck_detected_at = Column(DateTime, nullable=True)
    micro_step_exited_at = Column(DateTime, nullable=True)

    # Relationships
    micro_steps = relationship("MicroStep", back_populates="action_step", cascade="all, delete-orphan")
```

**ChatMessage Model Updates**
```python
class ChatMessage(Base):
    # ... existing fields ...

    triggered_micro_stepping = Column(Boolean, default=False, nullable=False)
```

### Definition of Done

- [ ] MicroStep model defined with all fields
- [ ] ActionStep model updated with scaffolding metadata
- [ ] ChatMessage model has trigger tracking field
- [ ] Alembic migration created and applied
- [ ] Relationships configured with cascade delete
- [ ] Models tested with CRUD operations

---

## Story 4.2: Build Stuck Detection Service

**As a** developer,
**I want** a service that identifies when users are genuinely stuck vs. lazy,
**so that** we only offer scaffolding when it's truly needed.

### Acceptance Criteria

1. `detectStuck` service function accepts: user message, action step, progress history (last 14 days), chat history (last 10 messages)
2. Function uses Gemini to analyze whether user is genuinely stuck based on criteria: repeated questions about same action step (3+ messages without progress), negative sentiment in messages, action step incomplete for 3+ days, user explicitly says "I'm stuck" or similar
3. Function distinguishes "stuck" from "lazy" by checking: if user completed other steps recently (active elsewhere = likely genuinely stuck on this one), if user is asking specific questions (engagement signal), if time estimate for step is unrealistic given user's context
4. Returns stuck assessment: `{ isStuck: boolean, confidence: 'high' | 'medium' | 'low', reason: string }`
5. If confidence is 'high' and isStuck is true, triggers micro-stepping offer
6. Manually tested with 5 "stuck" scenarios and 5 "lazy" scenarios, correctly identifies at least 7/10

### Technical Notes

- **Multi-Signal Analysis:** Chat sentiment + progress patterns + engagement indicators
- **AI-Powered:** Gemini analyzes stuck signals
- **Threshold:** Only offer scaffolding with "high" confidence

### System Prompt for Stuck Detection

```python
STUCK_DETECTION_PROMPT = """Analyze whether this user is genuinely stuck on their action step or just needs motivation.

Action Step: "{action_step_title}"
Description: {action_step_description}
Estimated Time: {estimated_minutes} minutes

User's latest message: "{user_message}"

Recent conversation (last {chat_count} messages):
{chat_history}

Progress context:
- Days since this step was created: {days_since_creation}
- Messages about this step: {message_count}
- Other steps completed recently: {other_completions}
- Total actions in last 7 days: {recent_actions}

Signs user is GENUINELY STUCK:
- Repeated specific questions about the same step (3+ messages)
- Expressing confusion about HOW to do something specific
- Step has been pending for 3+ days despite engagement
- Active on other steps but blocked on this one
- Asking for clarification on prerequisites or concepts

Signs user is NOT STUCK (just needs motivation):
- Generic "I don't feel like it" or "I'll do it later"
- No specific questions, just vague complaints
- No recent activity on ANY steps (inactive overall)
- Step just created (<1 day old, hasn't really tried yet)
- Asking for the answer instead of asking for guidance

Based on the evidence above, is this user genuinely stuck?

Respond with ONLY valid JSON:
{{
  "is_stuck": true/false,
  "confidence": "high" | "medium" | "low",
  "reason": "Brief explanation of your assessment"
}}
"""
```

### Service Function Signature

```python
async def detectStuck(
    user_message: str,
    action_step: ActionStep,
    user_id: UUID,
    chat_history: List[ChatMessage],
    progress_history: List[UserProgress]
) -> dict:
    """
    Detect if user is genuinely stuck vs. needs motivation.

    Args:
        user_message: User's latest message
        action_step: Current action step being discussed
        user_id: User ID for context
        chat_history: Recent chat messages (last 10)
        progress_history: User progress records (last 14 days)

    Returns:
        {
            "is_stuck": bool,
            "confidence": "high" | "medium" | "low",
            "reason": str
        }
    """
```

### Analysis Logic

```python
def analyze_stuck_signals(
    action_step: ActionStep,
    chat_history: List[ChatMessage],
    progress_history: List[UserProgress]
) -> dict:
    """
    Gather signals for stuck detection.

    Returns:
        {
            "days_since_creation": int,
            "message_count": int,  # Messages about this step
            "other_completions": int,  # Other steps completed recently
            "recent_actions": int,  # Total actions last 7 days
            "chat_count": int
        }
    """
    today = date.today()
    days_since_creation = (today - action_step.created_at.date()).days

    # Count messages about this action step
    message_count = sum(
        1 for msg in chat_history
        if msg.action_step_id == action_step.id
    )

    # Count other recent completions
    recent_actions = sum(p.actions_completed for p in progress_history[-7:])

    return {
        "days_since_creation": days_since_creation,
        "message_count": message_count,
        "other_completions": recent_actions,  # Simplified
        "recent_actions": recent_actions,
        "chat_count": len(chat_history)
    }
```

### Definition of Done

- [ ] detectStuck service function implemented
- [ ] Multi-signal analysis gathers context
- [ ] Gemini API call analyzes stuck vs. lazy
- [ ] Function returns structured assessment with confidence
- [ ] Manually tested with 10 scenarios (70%+ accuracy)
- [ ] Only triggers scaffolding with "high" confidence
- [ ] Error handling for API failures

---

## Story 4.3: Build Micro-Step Generation Service

**As a** developer,
**I want** a service that breaks action steps into 5-10 minute micro-tasks using Gemini,
**so that** overwhelming steps become manageable for stuck users.

### Acceptance Criteria

1. `generateMicroSteps` service function accepts action step (title, description, estimatedMinutes) and goal context
2. System prompt instructs Gemini to break action step into 3-8 micro-steps, each completable in 5-10 minutes, with very specific and concrete tasks
3. System prompt emphasizes micro-steps should be sequential (step 2 builds on step 1) and require no prerequisite knowledge user hasn't demonstrated
4. Function calls Gemini 1.5 Flash with action step context
5. Response parsed into array of micro-step titles: `[{ title, order }]`
6. Function creates MicroStep records in database linked to action step and returns array
7. Action step updated: microStepsGenerated = true, stuckDetectedAt = now
8. Manually tested with 3 complex action steps (e.g., "Set up development environment", "Write first function", "Deploy to cloud") and generates reasonable 5-10 min breakdowns

### Technical Notes

- **Granularity:** 5-10 minute micro-steps (vs. 5-30 minute action steps)
- **Sequential:** Each step builds on previous
- **Concrete:** Very specific tasks, no ambiguity

### System Prompt for Micro-Step Generation

```python
MICRO_STEP_GENERATION_PROMPT = """You are an expert learning scaffolding assistant. A user is stuck on an action step and needs it broken down into smaller, more manageable tasks.

Original Action Step:
Title: {action_step_title}
Description: {action_step_description}
Estimated Time: {estimated_minutes} minutes

Goal Context: {goal_title}

Your task: Break this action step into 3-8 micro-steps that are:
1. Each completable in 5-10 minutes (ultra-granular)
2. Sequential (step 2 assumes step 1 is done)
3. Concrete and specific (no ambiguous language)
4. Require NO prerequisite knowledge beyond what a beginner would have
5. Build confidence through small wins

Example (GOOD micro-steps for "Set up Python development environment"):
1. "Go to python.org and download Python 3.11 installer for your operating system"
2. "Run the installer and check the 'Add Python to PATH' checkbox before clicking Install"
3. "Open terminal/command prompt and type 'python --version' to verify installation"
4. "Download VS Code from code.visualstudio.com and install it"
5. "Open VS Code and install the Python extension from the Extensions marketplace"
6. "Create a new file called 'hello.py' and type: print('Hello, World!')"
7. "Run the file by clicking the green play button and confirm output appears"

Example (BAD micro-steps - too vague):
1. "Install Python"
2. "Set up your editor"
3. "Test your setup"

Return ONLY valid JSON:
{{
  "micro_steps": [
    {{"title": "Very specific micro-step 1", "order": 1}},
    {{"title": "Very specific micro-step 2", "order": 2}},
    ...
  ]
}}
"""
```

### Service Function Signature

```python
async def generateMicroSteps(
    action_step: ActionStep,
    goal: Goal
) -> List[MicroStep]:
    """
    Generate micro-steps for an action step using Gemini API.

    Args:
        action_step: Action step to break down
        goal: Parent goal for context

    Returns:
        List of created MicroStep objects

    Raises:
        GeminiAPIError: If API call fails
        ValidationError: If response format is invalid
    """
```

### Implementation

```python
async def generateMicroSteps(
    action_step: ActionStep,
    goal: Goal,
    db: AsyncSession
) -> List[MicroStep]:
    """Generate and persist micro-steps for action step."""

    # 1. Call Gemini API
    prompt = MICRO_STEP_GENERATION_PROMPT.format(
        action_step_title=action_step.title,
        action_step_description=action_step.description,
        estimated_minutes=action_step.estimated_minutes,
        goal_title=goal.title
    )

    response = await call_gemini_api(prompt)
    data = json.loads(response)

    # 2. Validate structure
    if "micro_steps" not in data or not isinstance(data["micro_steps"], list):
        raise ValidationError("Invalid micro-step structure")

    # 3. Create MicroStep records
    micro_steps = []
    async with db.begin():
        for item in data["micro_steps"]:
            micro_step = MicroStep(
                action_step_id=action_step.id,
                title=item["title"],
                order=item["order"],
                status="pending"
            )
            db.add(micro_step)
            micro_steps.append(micro_step)

        # 4. Update action step metadata
        action_step.micro_steps_generated = True
        action_step.stuck_detected_at = datetime.utcnow()

        await db.commit()

    return micro_steps
```

### Definition of Done

- [ ] generateMicroSteps service function implemented
- [ ] System prompt creates 5-10 minute micro-tasks
- [ ] Micro-steps are sequential and concrete
- [ ] MicroStep records created in database
- [ ] ActionStep metadata updated
- [ ] Manually tested with 3 complex action steps
- [ ] Generated micro-steps are reasonable and helpful
- [ ] Error handling for API failures and validation

---

## Story 4.4: Implement Micro-Stepping Offer in Chat

**As a** logged-in user,
**I want** the AI to detect when I'm stuck and offer to break down the step for me,
**so that** I get help when I need it without having to explicitly ask.

### Acceptance Criteria

1. Chat API endpoint (`POST /api/chat`) now includes stuck detection check after receiving user message
2. If `detectStuck` returns high confidence stuck status, AI response includes offer: "It seems like this step might be challenging. Would you like me to break it down into smaller 5-10 minute tasks?"
3. User can respond "yes" or click suggested action button "Break it down" (detected via message parsing or explicit button payload)
4. When user accepts, endpoint calls `generateMicroSteps` service and returns micro-step list in response
5. Chat interface displays micro-steps as interactive checklist within the conversation (not just text list)
6. User can mark micro-steps complete inline in chat (calls new `POST /api/micro-steps/:id/complete` endpoint)
7. When all micro-steps are completed, AI congratulates user and suggests marking the parent action step as complete
8. User can decline offer ("No thanks, I'll keep trying") - AI responds supportively and continues Socratic questioning
9. Stuck detection only triggers once per action step per 24 hours to avoid annoying user with repeated offers

### Technical Notes

- **Offer Trigger:** Stuck detection with "high" confidence
- **User Response Parsing:** Detect "yes", "break it down", "help me" etc.
- **Interactive UI:** Micro-steps as checkboxes in chat
- **Rate Limiting:** One offer per step per 24 hours

### Enhanced Chat Endpoint Logic

```python
@router.post("/chat")
async def chat_with_mentor(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # ... existing code ...

    # NEW: Check if user is stuck (if action step context provided)
    if request.action_step_id:
        action_step = await get_action_step(db, request.action_step_id)

        # Only check if micro-steps not already generated recently
        should_check_stuck = (
            not action_step.micro_steps_generated or
            (action_step.stuck_detected_at and
             (datetime.utcnow() - action_step.stuck_detected_at).days >= 1)
        )

        if should_check_stuck:
            stuck_assessment = await detectStuck(
                request.message,
                action_step,
                current_user.id,
                conversation_history,
                recent_progress
            )

            if stuck_assessment["is_stuck"] and stuck_assessment["confidence"] == "high":
                # Offer micro-stepping
                reply = "It seems like this step might be challenging. Would you like me to break it down into smaller 5-10 minute tasks that might be easier to tackle?"

                await save_chat_message(db, current_user.id, "mentor", reply, triggered_micro_stepping=True)

                return ChatResponse(
                    reply=reply,
                    ai_mode="mentor",
                    micro_stepping_offered=True,
                    action_step_id=action_step.id
                )

    # ... existing mentor/emotional support logic ...
```

### User Acceptance Detection

```python
def detect_micro_step_acceptance(user_message: str) -> bool:
    """
    Check if user is accepting micro-stepping offer.

    Returns True if message contains acceptance indicators.
    """
    acceptance_patterns = [
        r'\byes\b',
        r'\byeah\b',
        r'\bsure\b',
        r'\bokay\b',
        r'\bok\b',
        r'\bplease\b',
        r'break it down',
        r'help me',
        r'i would like',
    ]

    for pattern in acceptance_patterns:
        if re.search(pattern, user_message, re.IGNORECASE):
            return True
    return False
```

### Micro-Step Generation Response

```python
# When user accepts offer
if detect_micro_step_acceptance(request.message):
    # Generate micro-steps
    goal = await get_goal_for_action_step(db, action_step.id)
    micro_steps = await generateMicroSteps(action_step, goal, db)

    # Return micro-steps in response
    return ChatResponse(
        reply="Great! I've broken this down into smaller steps for you. Let's tackle them one at a time:",
        ai_mode="mentor",
        micro_steps=[
            {"id": str(ms.id), "title": ms.title, "order": ms.order, "status": ms.status}
            for ms in micro_steps
        ]
    )
```

### API Endpoint for Micro-Step Completion

**POST /api/micro-steps/:microStepId/complete**

```python
@router.post("/micro-steps/{micro_step_id}/complete")
async def complete_micro_step(
    micro_step_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark micro-step as completed and update progress."""
    async with db.begin():
        micro_step = await get_micro_step(db, micro_step_id, current_user.id)
        micro_step.status = "completed"
        micro_step.completed_at = datetime.utcnow()

        # Also update user progress (micro-steps count toward streak)
        today = date.today()
        progress = await get_or_create_progress(db, current_user.id, today)
        progress.actions_completed += 1
        progress.minutes_worked += 10  # Assume 10 min per micro-step

        await db.commit()

    # Check if all micro-steps completed
    all_micro_steps = await get_micro_steps_for_action(db, micro_step.action_step_id)
    all_completed = all(ms.status == "completed" for ms in all_micro_steps)

    return {
        "micro_step": micro_step,
        "all_completed": all_completed,
        "congrats_message": "🎉 Great job! All micro-steps completed. Ready to mark the main action step as complete?" if all_completed else None
    }
```

### Definition of Done

- [ ] Chat endpoint includes stuck detection check
- [ ] Micro-stepping offer generated for high-confidence stuck users
- [ ] User acceptance detected via message parsing
- [ ] generateMicroSteps called when user accepts
- [ ] Micro-steps returned in chat response
- [ ] POST /api/micro-steps/:id/complete endpoint implemented
- [ ] Chat UI displays micro-steps as interactive checklist
- [ ] Completion of all micro-steps triggers congratulations
- [ ] User can decline offer and continue Socratic questioning
- [ ] Rate limiting: one offer per step per 24 hours

---

## Story 4.5: Build Micro-Step Completion and Exit UI

**As a** logged-in user,
**I want** to work through micro-steps and exit scaffolding when I'm ready,
**so that** I maintain control over my learning process.

### Acceptance Criteria

1. When micro-steps are generated for an action step, goal detail page shows "🎯 Scaffolding Active" badge on that action step
2. Clicking action step expands inline view showing list of micro-steps with checkboxes
3. Checking micro-step checkbox calls `POST /api/micro-steps/:id/complete` and updates UI (strikethrough, timestamp)
4. Micro-step view includes "Exit Scaffolding" button that collapses micro-steps and returns to normal action step view
5. Clicking "Exit Scaffolding" updates action step: microStepExitedAt = now, hides micro-steps (still in DB but not shown)
6. If user exits scaffolding and becomes stuck again later, system can re-offer or generate new micro-steps (not just show old ones)
7. Progress calculation: Action step counts as complete only if parent action step is marked complete OR all micro-steps are completed
8. Streak tracking: Completing micro-steps counts toward daily actions completed (each micro-step increments counter)
9. Mobile responsive: Micro-step checklist stacks vertically with clear touch targets

### Technical Notes

- **Badge Indicator:** Show when micro-steps exist and not exited
- **Inline View:** Expandable section within action step
- **Exit Logic:** Hide micro-steps but keep in database for analytics

### UI Components

**Action Step with Scaffolding Badge**
```
┌─────────────────────────────────────────┐
│ ☐ Install Python development environment│
│   🎯 Scaffolding Active                  │
│   [Click to expand micro-steps]          │
└─────────────────────────────────────────┘
```

**Expanded Micro-Step View**
```
┌─────────────────────────────────────────┐
│ ☐ Install Python development environment│
│   🎯 Scaffolding Active                  │
│                                         │
│   Micro-steps:                          │
│   ☑ Download Python installer (done)    │
│   ☑ Run installer with PATH checkbox    │
│   ☐ Verify installation in terminal     │
│   ☐ Download and install VS Code        │
│   ☐ Install Python extension            │
│                                         │
│   [Exit Scaffolding] [✓ Mark Step Done] │
└─────────────────────────────────────────┘
```

**Chat Interface Micro-Steps**
```
AI: Great! I've broken this down for you:

┌─────────────────────────────────────────┐
│ ☑ Download Python installer             │
│ ☑ Run installer with PATH checkbox      │
│ ☐ Verify installation in terminal       │
│ ☐ Download and install VS Code          │
│ ☐ Install Python extension              │
└─────────────────────────────────────────┘

User: [checks a box]
AI: Excellent! You're making progress. Keep going!
```

### Component Implementation

**MicroStepList Component**
```typescript
function MicroStepList({ actionStepId, microSteps, onComplete, onExit }) {
  const handleCheck = async (microStepId: string) => {
    // Optimistic update
    const updatedSteps = microSteps.map(ms =>
      ms.id === microStepId ? { ...ms, status: 'completed' } : ms
    );

    try {
      await api.post(`/micro-steps/${microStepId}/complete`);
      onComplete(updatedSteps);

      // Check if all completed
      const allDone = updatedSteps.every(ms => ms.status === 'completed');
      if (allDone) {
        toast.success('🎉 All micro-steps completed!');
      }
    } catch (error) {
      // Rollback on error
      toast.error('Failed to complete step');
    }
  };

  return (
    <div className="micro-steps">
      <p className="text-sm text-gray-600 mb-2">Micro-steps:</p>
      {microSteps.map(ms => (
        <label key={ms.id} className="flex items-center gap-2 p-2 hover:bg-gray-50">
          <input
            type="checkbox"
            checked={ms.status === 'completed'}
            onChange={() => handleCheck(ms.id)}
          />
          <span className={ms.status === 'completed' ? 'line-through' : ''}>
            {ms.title}
          </span>
        </label>
      ))}
      <div className="flex gap-2 mt-4">
        <button onClick={onExit} className="btn-secondary">
          Exit Scaffolding
        </button>
        {microSteps.every(ms => ms.status === 'completed') && (
          <button className="btn-primary">
            ✓ Mark Step Done
          </button>
        )}
      </div>
    </div>
  );
}
```

### Exit Scaffolding API

**POST /api/action-steps/:stepId/exit-scaffolding**

```python
@router.post("/action-steps/{step_id}/exit-scaffolding")
async def exit_scaffolding(
    step_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Exit micro-stepping scaffolding mode."""
    async with db.begin():
        action_step = await get_action_step(db, step_id, current_user.id)
        action_step.micro_step_exited_at = datetime.utcnow()
        await db.commit()

    return {"message": "Scaffolding exited", "action_step_id": step_id}
```

### Definition of Done

- [ ] Scaffolding badge displayed when micro-steps active
- [ ] Action step expands to show micro-step checklist
- [ ] Micro-step checkboxes call completion API
- [ ] Optimistic UI updates with error rollback
- [ ] "Exit Scaffolding" button hides micro-steps
- [ ] Exit API updates microStepExitedAt timestamp
- [ ] All micro-steps completed triggers congratulations
- [ ] Micro-step completion counts toward daily streak
- [ ] Mobile responsive design with clear touch targets

---

## Story 4.6: Add Scaffolding Analytics and Feedback

**As a** product team,
**I want** basic analytics on scaffolding usage and effectiveness,
**so that** we can demonstrate the adaptive learning concept to competition judges.

### Acceptance Criteria

1. Database query to count: total users who received micro-stepping offer, acceptance rate, completion rate of micro-steps vs. parent action steps
2. Simple admin dashboard or script (`npm run analytics`) that outputs scaffolding metrics: offers made, accepted, declined, micro-steps completed, action steps completed via scaffolding
3. After user completes all micro-steps, AI asks: "How did breaking this down help? (Just curious!)" - captures qualitative feedback in chat
4. Feedback stored in ChatMessage and can be manually reviewed for testimonials
5. Metrics visible in simple markdown report (generated by script) for inclusion in competition pitch deck: "X% of stuck users accepted scaffolding, Y% completed their action step with our help"
6. No fancy dashboard UI needed - command-line output or markdown file sufficient for MVP

### Technical Notes

- **Analytics:** Simple database queries, no analytics service
- **Reporting:** Command-line script or markdown file
- **Qualitative Feedback:** AI asks for feedback after completion

### Analytics Queries

```python
# analytics.py script

async def generate_scaffolding_report(db: AsyncSession):
    """Generate scaffolding analytics report."""

    # 1. Count offers made
    offers_made = await db.execute(
        select(func.count(ChatMessage.id))
        .where(ChatMessage.triggered_micro_stepping == True)
    )
    total_offers = offers_made.scalar()

    # 2. Count acceptances (action steps with micro-steps generated)
    acceptances = await db.execute(
        select(func.count(ActionStep.id))
        .where(ActionStep.micro_steps_generated == True)
    )
    total_acceptances = acceptances.scalar()

    # 3. Count micro-step completions
    micro_completions = await db.execute(
        select(func.count(MicroStep.id))
        .where(MicroStep.status == "completed")
    )
    total_micro_completions = micro_completions.scalar()

    # 4. Count action steps completed after scaffolding
    scaffolded_completions = await db.execute(
        select(func.count(ActionStep.id))
        .where(
            ActionStep.micro_steps_generated == True,
            ActionStep.status == "completed"
        )
    )
    total_scaffolded_completions = scaffolded_completions.scalar()

    # Generate report
    acceptance_rate = (total_acceptances / total_offers * 100) if total_offers > 0 else 0
    completion_rate = (total_scaffolded_completions / total_acceptances * 100) if total_acceptances > 0 else 0

    report = f"""
# Scaffolding Analytics Report

Generated: {datetime.utcnow().isoformat()}

## Key Metrics

- **Micro-stepping offers made:** {total_offers}
- **Offers accepted:** {total_acceptances} ({acceptance_rate:.1f}%)
- **Micro-steps completed:** {total_micro_completions}
- **Action steps completed via scaffolding:** {total_scaffolded_completions} ({completion_rate:.1f}%)

## Insights

- **Acceptance Rate:** {acceptance_rate:.1f}% of stuck users accepted scaffolding help
- **Completion Rate:** {completion_rate:.1f}% of users who accepted scaffolding completed their action step
- **Average micro-steps per action:** {total_micro_completions / total_acceptances if total_acceptances > 0 else 0:.1f}

## Competition Pitch Points

> "{acceptance_rate:.0f}% of stuck users accepted our adaptive scaffolding, and {completion_rate:.0f}% successfully completed their goals with our help."

"""

    return report
```

### Feedback Collection

When user completes all micro-steps:

```python
# In complete_micro_step endpoint
if all_completed:
    # Send feedback request in chat
    feedback_message = "🎉 Congratulations on completing all the micro-steps! How did breaking this down help you? (Just curious - your feedback helps us improve!)"

    await save_chat_message(
        db, current_user.id, "mentor", feedback_message,
        goal_id=goal_id, action_step_id=action_step.id
    )
```

### CLI Script

```bash
# Run analytics
python scripts/generate_scaffolding_report.py > docs/scaffolding-report.md
```

### Definition of Done

- [ ] Analytics queries implemented
- [ ] Script generates scaffolding metrics
- [ ] Acceptance rate and completion rate calculated
- [ ] AI asks for feedback after micro-step completion
- [ ] Feedback stored in ChatMessage for manual review
- [ ] Report outputs to markdown file
- [ ] Competition-ready metrics (X% acceptance, Y% completion)
- [ ] No fancy UI needed - simple script sufficient

---

## Epic 4 Summary

### Stories Completed
- 6 stories total
- All P1 (nice-to-have - OPTIONAL)

### Key Deliverables
1. ✅ Extended database schema for micro-steps and scaffolding metadata
2. ✅ Stuck detection service (distinguishes genuinely stuck vs. lazy)
3. ✅ Micro-step generation service (breaks steps into 5-10 min tasks)
4. ✅ Micro-stepping offer in chat (automatic detection and offer)
5. ✅ Micro-step completion UI with exit option
6. ✅ Scaffolding analytics and feedback collection

### Core Features Implemented
- **Intelligent Stuck Detection:** Multi-signal analysis (chat + progress + engagement)
- **Adaptive Scaffolding:** Dynamic breakdown into 5-10 minute micro-tasks
- **User Agency:** Users can accept, decline, or exit scaffolding at any time
- **Progress Tracking:** Micro-step completion counts toward streaks
- **Analytics:** Measure scaffolding effectiveness for competition demo

### Technical Achievements
- AI-powered stuck detection with confidence scoring
- Context-aware micro-step generation using Gemini
- Interactive UI for micro-step management
- Graceful degradation (scaffolding is additive, not required)
- Analytics for demonstrating adaptive learning concept

### Competition Value
This epic showcases Apollo's unique adaptive scaffolding capability:
- **X% acceptance rate** of micro-stepping offers
- **Y% completion rate** for scaffolded action steps
- Demonstrates "AI that teaches, not tells" with concrete metrics
- Addresses productive struggle vs. unproductive friction distinction

### What's Next
With Epic 4 complete (if time allows), Apollo has a complete adaptive learning system. Epic 5 (optional) adds community and notes features for peer support and knowledge capture.

**Ready for Epic 5: Community & Notes (P1 - OPTIONAL)** 🚀

**⚠️ REMINDER:** Epic 4 is optional. If behind schedule, skip to competition preparation and demos.
