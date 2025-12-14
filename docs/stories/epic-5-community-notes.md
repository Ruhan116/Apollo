# Epic 5: Community & Notes

**Project:** Apollo
**Epic Goal:** Add goal-based community forums for peer support and simple note-taking functionality. This addresses the "loss of human interaction" problem by enabling users to connect with others working on similar goals and capture their learning insights.

**Priority:** P1 (Nice-to-Have - HIGHLY CUTTABLE)
**Estimated Timeline:** Days 21-24 of development (if schedule allows)
**Dependencies:** Epic 3 (Socratic Mentor AI & Progress Tracking)

**⚠️ NOTE:** This epic is highly cuttable. **CUT THIS ENTIRE EPIC if behind schedule on Dec 23.** Epics 1-3 deliver the core Apollo value proposition. Only implement if Epics 1-3 are completed ahead of schedule.

---

## Story 5.1: Design Database Schema for Forums and Notes

**As a** developer,
**I want** database models for forum posts, replies, and user notes,
**so that** we can persist community content and personal reflections.

### Acceptance Criteria

1. SQLAlchemy model defines `Forum` class with fields: id, title (e.g., "Learning Python", "Getting Fit"), slug (String, URL-friendly), description (Text), created_at (DateTime)
2. SQLAlchemy model defines `ForumPost` class with fields: id, forum_id (ForeignKey), user_id (ForeignKey), title, content (Text), upvotes (Integer, default 0), created_at, updated_at
3. SQLAlchemy model defines `ForumReply` class with fields: id, post_id (ForeignKey to ForumPost), user_id (ForeignKey), content (Text), created_at
4. SQLAlchemy model defines `Note` class with fields: id, user_id (ForeignKey), goal_id (ForeignKey), content (Text, markdown), created_at, updated_at
5. Alembic migration created and applied for all forum and note models
6. Can create forums, posts, replies, and notes via SQLAlchemy session

### Technical Notes

- **New Models:** Forum, ForumPost, ForumReply, Note
- **Slug:** URL-friendly identifier for forums (generated from title)
- **Markdown:** Notes stored as markdown text, rendered on frontend
- **Cascade Delete:** Posts delete when forum deleted, replies delete when post deleted, notes delete when goal deleted

### Database Schema

**Forum Model**
```python
class Forum(Base):
    __tablename__ = "forums"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False, unique=True)
    slug = Column(String(100), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    posts = relationship("ForumPost", back_populates="forum", cascade="all, delete-orphan")
    goals = relationship("Goal", back_populates="forum")
```

**ForumPost Model**
```python
class ForumPost(Base):
    __tablename__ = "forum_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    forum_id = Column(UUID(as_uuid=True), ForeignKey("forums.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    forum = relationship("Forum", back_populates="posts")
    user = relationship("User", back_populates="forum_posts")
    replies = relationship("ForumReply", back_populates="post", cascade="all, delete-orphan")
```

**ForumReply Model**
```python
class ForumReply(Base):
    __tablename__ = "forum_replies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("forum_posts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    post = relationship("ForumPost", back_populates="replies")
    user = relationship("User", back_populates="forum_replies")
```

**Note Model**
```python
class Note(Base):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    goal_id = Column(UUID(as_uuid=True), ForeignKey("goals.id", ondelete="CASCADE"), nullable=False, index=True)
    content = Column(Text, nullable=False)  # Markdown format
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="notes")
    goal = relationship("Goal", back_populates="notes")
```

**Goal Model Updates**
```python
class Goal(Base):
    # ... existing fields ...
    forum_id = Column(UUID(as_uuid=True), ForeignKey("forums.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships
    forum = relationship("Forum", back_populates="goals")
    notes = relationship("Note", back_populates="goal", cascade="all, delete-orphan")
```

### Definition of Done

- [ ] Forum, ForumPost, ForumReply, and Note models defined
- [ ] Goal model updated with forum_id field
- [ ] All relationships configured with appropriate cascade rules
- [ ] Alembic migration created and applied
- [ ] Models tested with CRUD operations
- [ ] Database indexes created on foreign keys

---

## Story 5.2: Implement Forum Creation and Post Management APIs

**As a** developer,
**I want** backend APIs for creating forums, posting, replying, and upvoting,
**so that** users can participate in goal-based communities.

### Acceptance Criteria

1. `GET /api/forums` endpoint returns list of all forums (public, no auth required)
2. `POST /api/forums` endpoint creates new forum (title, description) - admin/system only for MVP (hardcode check or skip auth), auto-generates slug from title
3. `GET /api/forums/:slug/posts` endpoint returns posts for forum sorted by upvotes descending, includes author email (for display), post count
4. `POST /api/forums/:slug/posts` endpoint creates post (requires auth, validates title and content not empty)
5. `POST /api/posts/:postId/upvote` endpoint increments post upvotes (requires auth, one upvote per user - store in separate UpVote join table or allow multiple for MVP simplicity)
6. `GET /api/posts/:postId/replies` endpoint returns replies for post with author info
7. `POST /api/posts/:postId/replies` endpoint creates reply (requires auth, validates content not empty)
8. Basic profanity filter applied to all post/reply content before saving (using better-profanity library)
9. Error handling for invalid forum slugs, missing posts, unauthorized access

### Technical Notes

- **Profanity Filter:** better-profanity 0.7.0 Python library
- **Slug Generation:** Convert title to lowercase, replace spaces with hyphens
- **Upvotes:** Simplified - allow multiple upvotes per user for MVP (no join table)
- **Public Forums:** GET /api/forums doesn't require auth

### API Endpoints

**GET /api/forums**
```json
Response (200 OK):
[
  {
    "id": "forum-uuid-1",
    "title": "Learning Python",
    "slug": "learning-python",
    "description": "Community for Python learners",
    "post_count": 42,
    "created_at": "2025-12-14T10:00:00Z"
  },
  {
    "id": "forum-uuid-2",
    "title": "Getting Fit",
    "slug": "getting-fit",
    "description": "Fitness and health goals",
    "post_count": 28,
    "created_at": "2025-12-13T09:00:00Z"
  }
]
```

**POST /api/forums** (Admin only for MVP)
```json
Request:
{
  "title": "Learning Python",
  "description": "Community for Python learners of all levels"
}

Response (201 Created):
{
  "id": "forum-uuid",
  "title": "Learning Python",
  "slug": "learning-python",
  "description": "Community for Python learners of all levels",
  "created_at": "2025-12-14T10:00:00Z"
}
```

**GET /api/forums/:slug/posts**
```json
Response (200 OK):
[
  {
    "id": "post-uuid-1",
    "title": "How do I debug my first program?",
    "content": "I'm stuck on...",
    "upvotes": 15,
    "reply_count": 8,
    "author": {
      "email": "user@example.com"
    },
    "created_at": "2025-12-14T09:00:00Z"
  }
]
```

**POST /api/forums/:slug/posts** (Auth required)
```json
Request:
{
  "title": "My first Python program worked!",
  "content": "I just wrote my first Hello World and it ran perfectly! Feeling so proud!"
}

Response (201 Created):
{
  "id": "post-uuid",
  "title": "My first Python program worked!",
  "content": "I just wrote my first Hello World...",
  "upvotes": 0,
  "author": {...},
  "created_at": "2025-12-14T10:00:00Z"
}
```

**POST /api/posts/:postId/upvote** (Auth required)
```json
Response (200 OK):
{
  "post_id": "post-uuid",
  "upvotes": 16
}
```

**GET /api/posts/:postId/replies**
```json
Response (200 OK):
[
  {
    "id": "reply-uuid-1",
    "content": "Great question! Have you tried...",
    "author": {
      "email": "helper@example.com"
    },
    "created_at": "2025-12-14T09:30:00Z"
  }
]
```

**POST /api/posts/:postId/replies** (Auth required)
```json
Request:
{
  "content": "Thanks for sharing! I had the same issue..."
}

Response (201 Created):
{
  "id": "reply-uuid",
  "content": "Thanks for sharing!...",
  "author": {...},
  "created_at": "2025-12-14T10:00:00Z"
}
```

### Profanity Filter Implementation

```python
from better_profanity import profanity

def filter_profanity(text: str) -> str:
    """
    Filter profanity from user-generated content.

    Raises ValueError if content contains profanity.
    """
    if profanity.contains_profanity(text):
        raise ValueError("Content contains inappropriate language. Please revise and try again.")
    return text
```

### Slug Generation

```python
import re

def generate_slug(title: str) -> str:
    """Generate URL-friendly slug from title."""
    slug = title.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)  # Remove special chars
    slug = re.sub(r'[\s_-]+', '-', slug)  # Replace spaces with hyphens
    slug = slug.strip('-')
    return slug
```

### Definition of Done

- [ ] GET /api/forums endpoint returns forum list
- [ ] POST /api/forums endpoint creates forums (admin only)
- [ ] Slug auto-generated from forum title
- [ ] GET /api/forums/:slug/posts returns posts sorted by upvotes
- [ ] POST /api/forums/:slug/posts creates posts with auth
- [ ] POST /api/posts/:postId/upvote increments upvotes
- [ ] GET /api/posts/:postId/replies returns replies
- [ ] POST /api/posts/:postId/replies creates replies
- [ ] Profanity filter applied to all posts and replies
- [ ] Error handling for invalid inputs and unauthorized access

---

## Story 5.3: Build Forum Browse and Post UI

**As a** logged-in user,
**I want** to browse forums related to my goals and post questions or progress updates,
**so that** I can connect with peers working on similar objectives.

### Acceptance Criteria

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

### Technical Notes

- **Markdown Rendering:** react-markdown 9.0.0
- **Styling:** Tailwind CSS with card-based design
- **Optimistic UI:** Update upvote count immediately, rollback on error
- **Navigation:** Next.js dynamic routes

### UI Screens

**Forums List (`/forums`)**
```
┌─────────────────────────────────────────┐
│  Community Forums                       │
├─────────────────────────────────────────┤
│  ┌────────────────┐  ┌────────────────┐│
│  │ Learning Python│  │ Getting Fit    ││
│  │ Python learners│  │ Fitness goals  ││
│  │ 42 posts       │  │ 28 posts       ││
│  └────────────────┘  └────────────────┘│
└─────────────────────────────────────────┘
```

**Forum Posts (`/forums/learning-python`)**
```
┌─────────────────────────────────────────┐
│  Learning Python                        │
│  [+ New Post]                           │
├─────────────────────────────────────────┤
│  ▲ 15  How do I debug my first program? │
│        I'm stuck on... (8 replies)      │
│        by user@example.com - 2 hours ago│
│                                         │
│  ▲ 12  My first program worked!         │
│        Just finished... (5 replies)     │
│        by learner@example.com - 1 day   │
└─────────────────────────────────────────┘
```

**Post Detail (`/forums/learning-python/posts/[id]`)**
```
┌─────────────────────────────────────────┐
│  ▲ 15  How do I debug my first program? │
│                                         │
│  I'm stuck on understanding why my code │
│  doesn't run. I followed the tutorial   │
│  but...                                 │
│                                         │
│  by user@example.com - 2 hours ago      │
├─────────────────────────────────────────┤
│  Replies (8)                            │
│                                         │
│  helper@example.com - 1 hour ago        │
│  Great question! Have you tried...      │
│                                         │
│  mentor@example.com - 30 min ago        │
│  I had the same issue. What helped...   │
├─────────────────────────────────────────┤
│  [Your reply here...              ]     │
│  [Post Reply]                           │
└─────────────────────────────────────────┘
```

### Components

**ForumCard Component**
```typescript
function ForumCard({ forum }) {
  return (
    <Link href={`/forums/${forum.slug}`}>
      <div className="forum-card p-6 border rounded-lg hover:shadow-lg">
        <h3 className="text-xl font-bold">{forum.title}</h3>
        <p className="text-gray-600 mt-2">{forum.description}</p>
        <p className="text-sm text-gray-500 mt-4">
          {forum.post_count} posts
        </p>
      </div>
    </Link>
  );
}
```

**PostCard Component**
```typescript
function PostCard({ post }) {
  const [upvotes, setUpvotes] = useState(post.upvotes);

  const handleUpvote = async () => {
    setUpvotes(upvotes + 1);  // Optimistic
    try {
      await api.post(`/posts/${post.id}/upvote`);
    } catch (error) {
      setUpvotes(upvotes);  // Rollback
      toast.error('Failed to upvote');
    }
  };

  return (
    <div className="post-card p-4 border rounded">
      <button onClick={handleUpvote} className="upvote-btn">
        ▲ {upvotes}
      </button>
      <h4 className="font-semibold">{post.title}</h4>
      <p className="text-gray-700 mt-2">
        {truncate(post.content, 150)}
      </p>
      <div className="text-sm text-gray-500 mt-2">
        {post.reply_count} replies · by {post.author.email} · {timeAgo(post.created_at)}
      </div>
    </div>
  );
}
```

### Definition of Done

- [ ] Navigation header includes "Community" link
- [ ] Forums list page displays forum cards
- [ ] Forum detail page shows posts sorted by upvotes
- [ ] "+ New Post" button visible when logged in
- [ ] Post creation form functional with markdown support
- [ ] Posts display with upvote button and reply count
- [ ] Upvote button works with optimistic UI
- [ ] Post detail page shows full content and replies
- [ ] Reply form functional
- [ ] Markdown rendered correctly (react-markdown)
- [ ] Mobile responsive design

---

## Story 5.4: Auto-Create Forums Based on User Goals

**As a** user creating goals,
**I want** forums to automatically exist for my goal categories,
**so that** I can immediately find relevant communities.

### Acceptance Criteria

1. When user creates goal via `POST /api/goals`, backend extracts goal category from title/description using Gemini (ask "What category is this goal? Options: Learning/Programming, Fitness/Health, Career/Professional, Creative/Arts, Personal/Habits, Other")
2. System checks if forum for that category already exists (by slug), creates new forum if not found
3. Goal record includes optional `forumId` field linking to relevant forum
4. Goal detail page shows "💬 Join the [Category] Community" link to relevant forum if forumId exists
5. Forums page shows "Recommended for You" section at top highlighting forums matching user's active goal categories
6. If Gemini categorization fails, default to generic "General Goals" forum
7. Maximum 20 forums to avoid fragmentation (if category doesn't match existing 20, assign to closest match or "Other")

### Technical Notes

- **Auto-Creation:** Create forums on-demand when goals are created
- **Gemini Categorization:** Quick category extraction
- **Link Goals to Forums:** forumId field on Goal model

### Category Extraction Prompt

```python
GOAL_CATEGORIZATION_PROMPT = """Categorize this goal into ONE of the following categories:

1. Learning/Programming
2. Fitness/Health
3. Career/Professional
4. Creative/Arts
5. Personal/Habits
6. Other

Goal: {goal_title}
Description: {goal_description}

Respond with ONLY the category name (e.g., "Learning/Programming").
"""
```

### Auto-Forum Creation Logic

```python
async def create_or_get_forum(category: str, db: AsyncSession) -> Forum:
    """
    Get existing forum for category or create new one.

    Returns Forum object.
    """
    slug = generate_slug(category)

    # Check if forum exists
    result = await db.execute(
        select(Forum).where(Forum.slug == slug)
    )
    forum = result.scalar_one_or_none()

    if forum:
        return forum

    # Create new forum
    descriptions = {
        "learning-programming": "Community for learners tackling programming and technical skills",
        "fitness-health": "Support group for fitness, health, and wellness goals",
        "career-professional": "Professional development and career growth discussions",
        "creative-arts": "Creative projects, art, music, and creative pursuits",
        "personal-habits": "Building better habits and personal development",
        "other": "General goal discussions and support"
    }

    forum = Forum(
        title=category,
        slug=slug,
        description=descriptions.get(slug, f"Community for {category} goals")
    )
    db.add(forum)
    await db.commit()

    return forum
```

### Enhanced Goal Creation Endpoint

```python
@router.post("/goals")
async def create_goal(
    request: GoalCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # ... existing goal creation logic ...

    # NEW: Categorize and link to forum
    category = await categorize_goal(request.title, request.description)
    forum = await create_or_get_forum(category, db)

    goal.forum_id = forum.id
    await db.commit()

    return goal
```

### UI Enhancements

**Goal Detail Page - Forum Link**
```tsx
{goal.forum && (
  <div className="forum-link mt-4 p-4 bg-blue-50 border border-blue-200 rounded">
    <p className="text-sm">
      💬 Connect with others working on similar goals!
    </p>
    <Link href={`/forums/${goal.forum.slug}`} className="text-blue-600 font-semibold">
      Join the {goal.forum.title} Community →
    </Link>
  </div>
)}
```

**Forums Page - Recommended Section**
```tsx
{recommendedForums.length > 0 && (
  <section className="mb-8">
    <h2 className="text-2xl font-bold mb-4">Recommended for You</h2>
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {recommendedForums.map(forum => (
        <ForumCard key={forum.id} forum={forum} recommended />
      ))}
    </div>
  </section>
)}
```

### Definition of Done

- [ ] Goal categorization using Gemini implemented
- [ ] Auto-create forums for new categories
- [ ] Goal linked to forum via forumId
- [ ] Goal detail page shows forum link
- [ ] Forums page shows recommended forums
- [ ] Fallback to "General Goals" if categorization fails
- [ ] Maximum 20 forums enforced
- [ ] Forum descriptions appropriate for each category

---

## Story 5.5: Implement Note-Taking Functionality

**As a** logged-in user,
**I want** to capture insights and reflections as I work on my goals,
**so that** I can build a personal knowledge base and track my learning.

### Acceptance Criteria

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

### Technical Notes

- **Markdown Storage:** Store as plain markdown text
- **Rendering:** react-markdown on frontend
- **Privacy:** Notes are user-specific, not shared
- **Auto-save:** Debounced save on blur (500ms delay)

### API Endpoints

**POST /api/goals/:goalId/notes**
```json
Request:
{
  "content": "# Day 1 Learnings\n\nToday I learned about Python variables..."
}

Response (201 Created):
{
  "id": "note-uuid",
  "goal_id": "goal-uuid",
  "content": "# Day 1 Learnings...",
  "created_at": "2025-12-14T10:00:00Z",
  "updated_at": "2025-12-14T10:00:00Z"
}
```

**GET /api/goals/:goalId/notes**
```json
Response (200 OK):
[
  {
    "id": "note-uuid-1",
    "content": "# Day 1 Learnings...",
    "created_at": "2025-12-14T10:00:00Z",
    "updated_at": "2025-12-14T10:00:00Z"
  },
  {
    "id": "note-uuid-2",
    "content": "# Day 2 Progress...",
    "created_at": "2025-12-13T09:00:00Z",
    "updated_at": "2025-12-13T09:00:00Z"
  }
]
```

**PATCH /api/notes/:noteId**
```json
Request:
{
  "content": "# Day 1 Learnings (Updated)\n\nToday I learned..."
}

Response (200 OK):
{
  "id": "note-uuid",
  "content": "# Day 1 Learnings (Updated)...",
  "updated_at": "2025-12-14T11:00:00Z"
}
```

**DELETE /api/notes/:noteId**
```
Response (204 No Content)
```

### UI Components

**Notes Section (Collapsible)**
```
┌─────────────────────────────────────────┐
│  📝 Notes                        [+Add] │
├─────────────────────────────────────────┤
│  ┌───────────────────────────────────┐  │
│  │ # Day 2 Progress                  │  │
│  │                                   │  │
│  │ Today I completed the first...    │  │
│  │                                   │  │
│  │ 1 day ago  [Edit] [Delete]        │  │
│  └───────────────────────────────────┘  │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │ # Day 1 Learnings                 │  │
│  │                                   │  │
│  │ Started learning about variables...│  │
│  │                                   │  │
│  │ 2 days ago  [Edit] [Delete]       │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**Note Editor**
```
┌─────────────────────────────────────────┐
│  Add Note                               │
├─────────────────────────────────────────┤
│  [Write] [Preview]                      │
│                                         │
│  # Day 3 Reflections                    │
│                                         │
│  Today was challenging but I learned... │
│                                         │
│  - Key insight 1                        │
│  - Key insight 2                        │
│                                         │
│  [Cancel] [Save Note]                   │
└─────────────────────────────────────────┘
```

### Note Component

```typescript
function NoteEditor({ goalId, note = null, onSave, onCancel }) {
  const [content, setContent] = useState(note?.content || '');
  const [mode, setMode] = useState<'write' | 'preview'>('write');
  const debouncedSave = useDebouncedCallback(
    async (value: string) => {
      if (note) {
        await api.patch(`/notes/${note.id}`, { content: value });
      }
    },
    500
  );

  const handleSave = async () => {
    if (note) {
      await api.patch(`/notes/${note.id}`, { content });
    } else {
      await api.post(`/goals/${goalId}/notes`, { content });
    }
    onSave();
  };

  return (
    <div className="note-editor">
      <div className="tabs">
        <button onClick={() => setMode('write')}>Write</button>
        <button onClick={() => setMode('preview')}>Preview</button>
      </div>

      {mode === 'write' ? (
        <textarea
          value={content}
          onChange={(e) => {
            setContent(e.target.value);
            debouncedSave(e.target.value);
          }}
          className="w-full h-64 p-4 border rounded"
          placeholder="# My Note Title\n\nWrite your reflections here..."
        />
      ) : (
        <div className="markdown-preview p-4 border rounded">
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      )}

      <div className="actions mt-4">
        <button onClick={onCancel}>Cancel</button>
        <button onClick={handleSave} className="btn-primary">
          Save Note
        </button>
      </div>
    </div>
  );
}
```

### Definition of Done

- [ ] POST /api/goals/:goalId/notes endpoint creates notes
- [ ] GET /api/goals/:goalId/notes returns notes
- [ ] PATCH /api/notes/:noteId updates notes
- [ ] DELETE /api/notes/:noteId deletes notes
- [ ] Authorization prevents unauthorized edits
- [ ] Notes section on goal detail page
- [ ] "+ Add Note" button opens editor
- [ ] Markdown editor with write/preview tabs
- [ ] Notes rendered with react-markdown
- [ ] Auto-save on blur (debounced)
- [ ] Edit and delete functionality works
- [ ] Notes private to user

---

## Story 5.6: Add Content Moderation and Community Guidelines

**As a** product team,
**I want** basic content moderation to prevent spam and abuse in forums,
**so that** the community remains supportive and safe.

### Acceptance Criteria

1. Profanity filter applied to all forum posts and replies before saving (already in Story 5.2)
2. `/community-guidelines` page with simple rules: Be respectful, No spam, Support others, Stay on topic
3. Post/reply forms include checkbox: "I agree to community guidelines" (required before submission)
4. Rate limiting on forum posts: Max 10 posts per user per day, max 20 replies per user per day
5. "Report" button on posts/replies (for future moderation, just logs to database for MVP - no action taken)
6. Admin can manually delete posts/replies via direct database access (no UI needed for MVP)
7. If user's post is rejected by profanity filter, show error: "Your post contains inappropriate language. Please revise and try again."

### Technical Notes

- **Profanity Filter:** Already implemented in Story 5.2
- **Rate Limiting:** slowapi per-user limits
- **Report:** Simple logging, no action for MVP
- **Admin Moderation:** Manual database queries (no UI)

### Community Guidelines Page

**`/community-guidelines` Content**

```markdown
# Apollo Community Guidelines

Welcome to the Apollo community! Our forums are a place for learners to support each other, share progress, and ask questions.

## Core Principles

**Be Respectful**
- Treat all community members with kindness and respect
- No personal attacks, harassment, or bullying
- Respect different learning paces and approaches

**Support Others**
- Share your experiences to help fellow learners
- Provide constructive feedback, not criticism
- Celebrate others' wins and progress

**Stay On Topic**
- Keep discussions related to goal achievement and learning
- No spam, self-promotion, or off-topic content
- Use appropriate forums for your topic

**No Cheating**
- Don't ask for complete solutions or answers
- Help others learn, don't do the work for them
- Share guidance, not shortcuts

## Moderation

Posts containing profanity, spam, or violations of these guidelines may be removed. Repeated violations may result in account restrictions.

If you see content that violates these guidelines, please use the "Report" button.

## Questions?

Contact us at support@apollo.example.com
```

### Rate Limiting Implementation

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/forums/{slug}/posts")
@limiter.limit("10/day")  # Max 10 posts per day
async def create_post(...):
    ...

@router.post("/posts/{post_id}/replies")
@limiter.limit("20/day")  # Max 20 replies per day
async def create_reply(...):
    ...
```

### Report Button (Logging Only)

**Database Model for Reports**
```python
class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    post_id = Column(UUID(as_uuid=True), ForeignKey("forum_posts.id"), nullable=True)
    reply_id = Column(UUID(as_uuid=True), ForeignKey("forum_replies.id"), nullable=True)
    reason = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
```

**Report Endpoint**
```python
@router.post("/posts/{post_id}/report")
async def report_post(
    post_id: UUID,
    reason: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Log report for manual review."""
    report = Report(
        reporter_user_id=current_user.id,
        post_id=post_id,
        reason=reason
    )
    db.add(report)
    await db.commit()

    return {"message": "Report submitted. Thank you for helping keep our community safe."}
```

### UI Components

**Guidelines Checkbox**
```tsx
<label className="flex items-center gap-2 mt-4">
  <input
    type="checkbox"
    checked={agreedToGuidelines}
    onChange={(e) => setAgreedToGuidelines(e.target.checked)}
    required
  />
  <span className="text-sm">
    I agree to the{' '}
    <Link href="/community-guidelines" className="text-blue-600">
      Community Guidelines
    </Link>
  </span>
</label>
```

**Report Button**
```tsx
<button
  onClick={() => handleReport(post.id)}
  className="text-sm text-gray-500 hover:text-red-600"
>
  Report
</button>
```

### Definition of Done

- [ ] Profanity filter applied to posts and replies
- [ ] /community-guidelines page created with rules
- [ ] Post/reply forms require guidelines agreement
- [ ] Rate limiting: 10 posts/day, 20 replies/day per user
- [ ] Report button on posts and replies
- [ ] Report endpoint logs to database
- [ ] Error message for profanity filter rejection
- [ ] Admin can delete via database (no UI needed)

---

## Epic 5 Summary

### Stories Completed
- 6 stories total
- All P1 (nice-to-have - OPTIONAL)

### Key Deliverables
1. ✅ Database schema for forums, posts, replies, and notes
2. ✅ Forum and post management APIs
3. ✅ Forum browse and post UI
4. ✅ Auto-forum creation based on goal categories
5. ✅ Note-taking functionality with markdown support
6. ✅ Content moderation and community guidelines

### Core Features Implemented
- **Goal-Based Forums:** Auto-created communities for different goal types
- **Peer Support:** Post questions, share progress, get community help
- **Upvoting System:** Surface valuable content
- **Note-Taking:** Private markdown notes for capturing insights
- **Content Moderation:** Profanity filtering, rate limiting, reporting
- **Community Guidelines:** Clear expectations for respectful interaction

### Technical Achievements
- Auto-categorization using Gemini API
- Markdown support for rich content
- Optimistic UI for upvotes
- Profanity filtering with better-profanity
- Rate limiting to prevent spam
- Private user notes with auto-save

### Competition Value (If Implemented)
- Addresses "loss of human interaction" in solo AI learning
- Demonstrates peer community integration
- Shows comprehensive learning platform (AI mentor + community + personal notes)
- Differentiator: Goal-based forums (not generic discussion boards)

### What's Next
With Epic 5 complete (if time allows), Apollo has a full-featured learning platform with AI mentorship, adaptive scaffolding, peer community, and knowledge capture tools.

**⚠️ CRITICAL REMINDER:** Epic 5 is highly optional. If behind schedule by Dec 23, focus on competition prep:
- Polish Epics 1-3 (core value prop)
- Prepare demo scenarios
- Create pitch deck with analytics
- Test end-to-end user flows

**Ready for Competition Submission!** 🎉🏆
