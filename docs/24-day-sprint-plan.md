# Apollo: 24-Day Sprint Plan

**Competition Deadline:** December 28, 2025
**Team Size:** 3 members
**Start Date:** December 4, 2025

---

## 🎯 Critical Success Factors

1. **Ship working demo** - Judges need to SEE the Socratic AI in action
2. **Prove differentiation** - Must show why Apollo ≠ ChatGPT
3. **Compelling pitch** - Story + demo + vision in <5 min video
4. **Technical credibility** - Code that works, not vapor ware

---

## 📅 Sprint Breakdown (8 Sprints x 3 Days)

### Sprint 1: Dec 4-6 (Foundation)

**Goals:** Setup + Core Architecture + Role Assignment

**Day 1 (Dec 4) - TODAY:**
- [ ] Team meeting: Assign roles (Person A: Frontend, Person B: Backend/AI, Person C: Design/Pitch)
- [ ] Review brief and brainstorming docs together
- [ ] Initialize Git repo, project structure
- [ ] Get API keys (OpenAI or Anthropic, explore Azure OpenAI Service if available)
- [ ] Setup Azure account, claim student credits if eligible
	- [ ] Decide tech stack (recommend: Next.js frontend + FastAPI backend + Azure PostgreSQL OR Next.js frontend + FastAPI backend + Azure Cosmos DB)

**Day 2 (Dec 5):**
- [ ] Setup development environment (all 3 people)
	- [ ] Create basic project skeleton (Next.js frontend, FastAPI backend, database schema)
	- [ ] Explore Azure deployment options (App Service vs Static Web Apps + FastAPI on App Service or Containers)
- [ ] Draft system prompts for Mentor AI (Person B)
- [ ] Start wireframes for 3 core screens (Person C): Goal input, AI chat, Progress view
- [ ] Competitive analysis research (Person A or C)

**Day 3 (Dec 6):**
- [ ] Database schema finalized (users, goals, action_steps, messages, streaks)
- [ ] Setup Azure Database for PostgreSQL (or Cosmos DB) - Free/Basic tier
- [ ] Basic auth flow (signup/login) - use Azure AD B2C, Auth0, or Clerk
- [ ] Test first AI call (simple echo bot to verify API works)
- [ ] Wireframes complete and reviewed by team

**Sprint 1 Deliverable:** Development environment ready, basic auth working, AI API tested, designs approved

---

### Sprint 2: Dec 7-9 (Goal Creation Flow)

**Goals:** User can input goal, AI generates Harada plan

**Day 4 (Dec 7):**
- [ ] Build goal input UI (form with text area)
- [ ] Create API endpoint: `/api/generate-plan` (calls LLM)
- [ ] Implement Harada plan generation prompt (flexible structure)
- [ ] Store generated plan in database

**Day 5 (Dec 8):**
- [ ] Display generated plan to user (goals + action steps)
- [ ] Add "Request changes" button (user can ask AI to modify)
- [ ] Implement modification flow (user types feedback, AI regenerates)
- [ ] Test with 3-5 different goal types

**Day 6 (Dec 9):**
- [ ] Polish goal creation UX (loading states, error handling)
- [ ] Add confirmation step ("Accept this plan?")
- [ ] Save accepted plan and set user's active goal
- [ ] Test end-to-end: Signup → Create goal → Accept plan

**Sprint 2 Deliverable:** Working goal creation flow (input → AI generates plan → user accepts)

---

### Sprint 3: Dec 10-12 (Socratic AI Chat)

**Goals:** Core differentiator - AI that asks questions, doesn't give answers

**Day 7 (Dec 10):**
- [ ] Build chat UI (action step selected, chat interface appears)
- [ ] Create Mentor AI system prompt (Socratic mode - ask questions, guide thinking)
- [ ] Implement `/api/chat` endpoint (stores conversation history)
- [ ] Test: User asks "how do I learn Python?" - AI should ask clarifying questions

**Day 8 (Dec 11):**
- [ ] Add conversation context (AI knows which action step user is working on)
- [ ] Implement "What have you tried?" trigger when user seems lazy
- [ ] Create Emotional AI system prompt (encouragement, empathy)
- [ ] Test AI switching (Mentor → Emotional when frustration detected)

**Day 9 (Dec 12):**
- [ ] Refine system prompts based on testing (this is CRITICAL)
- [ ] Add "stuck" detection logic (simple version: keyword matching + conversation length)
- [ ] Implement micro-stepping: AI breaks current step into 3-5 smaller steps
- [ ] Test with real scenarios (lazy question vs. genuine struggle)

**Sprint 3 Deliverable:** Socratic AI chat working - refuses direct answers, asks guiding questions, detects stuck users

---

### Sprint 4: Dec 13-15 (Progress Tracking & Streaks)

**Goals:** Habit formation features - streaks, daily check-ins, progress visualization

**Day 10 (Dec 13):**
- [ ] Build progress dashboard UI (list of goals, action steps, completion status)
- [ ] Add "Mark as complete" button for action steps
- [ ] Implement streak calculation (consecutive days with at least 1 action step worked on)
- [ ] Display streak prominently on dashboard

**Day 11 (Dec 14):**
- [ ] Create "Today's focus" view (what are you working on today?)
- [ ] Add daily check-in prompt (appears on login if not done today)
- [ ] Implement progress history tracking (database: user_activity table)
- [ ] Visual progress indicator (e.g., progress bar per goal)

**Day 12 (Dec 15):**
- [ ] Add streak notifications/encouragement ("You're on a 7-day streak!")
- [ ] Implement "Don't break the chain" messaging when at risk
- [ ] Polish progress UI (make it motivating, not just data)
- [ ] Test: Can a user maintain a 3-day streak?

**Sprint 4 Deliverable:** Progress tracking + streak system working, users see their momentum

---

### Sprint 5: Dec 16-18 (Community Features - SIMPLIFIED)

**Goals:** Human connection element (decide: forums OR simple progress feed)

**DECISION POINT:** Full forums are complex. Consider simplified version.

**Option A: Full Forums (More impressive but riskier)**
- Day 13-15: Build forum infrastructure, posts, replies, upvotes

**Option B: Progress Feed (Safer for timeline)** ⭐ RECOMMENDED
- Day 13: Simple "Share progress" button (posts to public feed)
- Day 14: Feed view showing others' updates ("Alice completed 'Learn Python basics'!")
- Day 15: Add simple reactions (👏, 🔥) and comments

**Day 13 (Dec 16):**
- [ ] Choose Option A or B as a team
- [ ] Build basic infrastructure (posts table in database)
- [ ] Create post submission UI
- [ ] Display feed of recent posts

**Day 14 (Dec 17):**
- [ ] Add user interactions (reactions or replies)
- [ ] Implement basic moderation (profanity filter library)
- [ ] Style feed to be visually appealing

**Day 15 (Dec 18):**
- [ ] Seed feed with test data (10-15 realistic posts)
- [ ] Test community feature with team
- [ ] Polish UX (empty states, loading states)

**Sprint 5 Deliverable:** Community feature working (either forums or progress feed)

---

### Sprint 6: Dec 19-21 (Polish & Integration)

**Goals:** Everything works together, bug fixes, user testing

**Day 16 (Dec 19):**
- [ ] End-to-end testing: Signup → Goal → Chat → Complete step → See streak → Community
- [ ] Fix critical bugs discovered
- [ ] Add simple note-taking (text area per goal, save to DB)
- [ ] Ensure mobile responsive (test on phones)

**Day 17 (Dec 20):**
- [ ] User testing with 3-5 people outside the team
- [ ] Collect feedback, prioritize fixes
- [ ] Improve error handling and edge cases
- [ ] Performance optimization (AI response time, page loads)

**Day 18 (Dec 21):**
- [ ] Final bug fixes from user testing
- [ ] Polish UI/UX (consistent styling, smooth interactions)
- [ ] Add onboarding flow (first-time user experience)
- [ ] Prepare demo accounts with realistic data

**Sprint 6 Deliverable:** Polished, integrated product ready for demo recording

---

### Sprint 7: Dec 22-24 (Competition Materials)

**Goals:** Pitch video, demo script, documentation, submission prep

**Day 19 (Dec 22):**
- [ ] Write pitch script (problem → solution → demo → vision)
- [ ] Create demo scenario (realistic user journey that showcases Socratic AI)
- [ ] Design pitch deck slides (if needed for video)
- [ ] Practice pitch delivery (Person C leads, all contribute)

**Day 20 (Dec 23):**
- [ ] Record demo video (screen recording of Apollo in action)
- [ ] Record pitch video (team member presenting)
- [ ] Edit videos (tools: iMovie, DaVinci Resolve, or Descript)
- [ ] Create technical documentation (architecture diagram, setup instructions)

**Day 21 (Dec 24):**
- [ ] Final video edits and polish
- [ ] Prepare GitHub repo (clean up code, add README)
- [ ] Write project description for submission
- [ ] Review submission requirements checklist

**Sprint 7 Deliverable:** Pitch video, demo video, technical docs complete

---

### Sprint 8: Dec 25-27 (Submission & Buffer)

**Goals:** Submit + last-minute fixes + buffer for unexpected issues

**Day 22 (Dec 25):**
- [ ] Final review of all submission materials
- [ ] Test submission process (upload videos, links, etc.)
- [ ] Fix any last-minute critical bugs
- [ ] Prepare live demo environment (deployed URL working)

**Day 23 (Dec 26):**
- [ ] Submit to Microsoft Imagine Cup portal
- [ ] Verify submission received
- [ ] Create backup copies of all materials
- [ ] Deploy to Azure (App Service for backend, Static Web Apps for frontend, or single App Service for full-stack)

**Day 24 (Dec 27):**
- [ ] BUFFER DAY for emergencies
- [ ] Final testing of deployed app
- [ ] Prepare for potential live demo/judging (if applicable)
- [ ] Team celebration 🎉

**Sprint 8 Deliverable:** Submitted to competition, app deployed and stable

---

## 🚨 Risk Mitigation

**What if we fall behind?**
1. **Cut community features** - Focus on core Socratic AI (that's the differentiator)
2. **Simplify progress tracking** - Basic streak counter, skip fancy visualizations
3. **Skip note-taking** - Not essential for demo
4. **Use template UI** - Don't build from scratch, use Tailwind UI or similar

**Daily Standup (15 min):**
- What did I do yesterday?
- What am I doing today?
- Any blockers?

**Red Flags:**
- Day 9 and Socratic AI not working → ESCALATE
- Day 15 and no end-to-end flow → CUT SCOPE
- Day 21 and no video draft → ALL HANDS ON DECK

---

## 🎯 Absolute Must-Haves for Demo

These CANNOT be cut:

1. ✅ User can create a goal
2. ✅ AI generates personalized Harada plan
3. ✅ Socratic AI chat (refuses direct answers, asks questions)
4. ✅ AI detects when user is stuck and provides micro-steps
5. ✅ Basic progress tracking (complete steps)
6. ✅ Streak counter (shows consecutive days)
7. ✅ Clean, functional UI (doesn't need to be beautiful, just usable)
8. ✅ Pitch video showing the vision

**Nice-to-Haves (cut if behind):**
- Community features
- Note-taking
- Advanced emotion detection
- Polished animations/design

---

## ☁️ Azure Deployment Guide (Quick Reference)

**Recommended Azure Stack for Apollo:**

**Option A: Simple (Recommended for 24-day timeline)**
- **Azure App Service** (Web App) - Hosts the FastAPI backend; Next.js frontend can be hosted in the same App Service or on Azure Static Web Apps
- **Azure Database for PostgreSQL** - Flexible Server (Basic tier)
- **Standard OpenAI/Anthropic API** - External (simpler than Azure OpenAI setup)

**Option B: Advanced (If time permits)**
- **Azure Static Web Apps** - Frontend (Next.js static)
- **FastAPI backend** - Host on Azure App Service or as a container (App Service / ACI / Web App for Containers)
- **Azure Database for PostgreSQL** - Managed database
- **Azure OpenAI Service** - If available in your region (GPT-4 access)

**Free/Student Credits:**
- Microsoft Imagine Cup participants often get Azure credits
- Azure for Students: $100 credit (no credit card needed)
- Free tier: App Service F1 (free), PostgreSQL Basic tier (~$25/mo)

**Deployment Steps (Day 23-24):**
1. Create Azure App Service (or Static Web App)
2. Configure environment variables (DB connection, API keys)
3. Setup GitHub Actions for CI/CD (Azure provides templates)
4. Deploy database schema to Azure PostgreSQL
5. Test deployed app thoroughly
6. Configure custom domain (optional: apollo.azurewebsites.net works)

**Key Azure Resources:**
- Azure Portal: portal.azure.com
- Azure for Students: azure.microsoft.com/en-us/free/students
- Quickstart guides: docs.microsoft.com/azure

---

## 📊 Success Metrics for Demo

**Judge Questions You Must Answer:**
1. How is this different from ChatGPT? → Show Socratic AI refusing to answer
2. Does it actually help learning? → Show micro-stepping when stuck
3. Can it scale? → Explain community + peer support
4. Why will people use it? → Show streak motivation, self-chosen goals
5. What's your business model? → Mention freemium/subscription plan

**Demo Flow (3 minutes):**
1. Problem statement (30 sec): AI gives answers → no learning
2. Solution intro (30 sec): Apollo guides, doesn't solve
3. Live demo (90 sec): Create goal → AI asks Socratic questions → Get stuck → Micro-steps → Complete task → See streak
4. Vision (30 sec): Scale to millions, become anti-ChatGPT for learning

---

## 💪 Team Motivation

**You have 24 days to build something that matters.**

This isn't just a competition - you're solving a real problem. AI is making people lazy learners. Apollo can make them stronger thinkers.

**Stay focused. Ship fast. Cut ruthlessly. You've got this.** 🚀

---

*Sprint plan created for Apollo - Microsoft Imagine Cup 2025*
