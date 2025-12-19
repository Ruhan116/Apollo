from app.repositories.goals import GoalRepository, SubgoalRepository, ActionRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.prompts.system import SYS_PROMPT
from app.models.goals import Goal, SubGoal, Actions, GoalStatus, SubgoalCategory
from google import genai
import json
from typing import Dict, List, Tuple, Optional


class GoalService:
    def __init__(self, db: AsyncSession):
        self.goal_repo = GoalRepository(db)
        self.subgoal_repo = SubgoalRepository(db)
        self.action_repo = ActionRepository(db)
        self.db = db 
        self.client = genai.Client()
    
    def make_llm_request(self, prompt: str) -> str:
        """Make a request to the LLM and return the response text."""
        response = self.client.models.generate_content(
            model="gemini-3-pro-preview",
            contents=SYS_PROMPT + "\n\nUser Goal: " + prompt,
        )
        return response.text
    
    def parse_response(self, response_text: str) -> Tuple[Dict, List[Dict], List[Dict]]:
        """Parse LLM response into goal, subgoals, and actions."""
        cleaned_text = response_text.strip()
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        if cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()
        
        # Parse JSON
        data = json.loads(cleaned_text)
        
        # Extract goal data
        goal_data = {
            "title": data.get("Goal", "Untitled Goal"),
            "description": data.get("Goal", "")
        }
        
        # Extract subgoals and actions
        subgoals_data = []
        actions_data = []
        
        for idx, subgoal in enumerate(data.get("subGoals", [])):
            subgoal_dict = {
                "title": subgoal.get("title", f"Subgoal {idx + 1}"),
                "description": subgoal.get("title", ""),
                "category": self._determine_category(idx, len(data.get("subGoals", [])))
            }
            subgoals_data.append(subgoal_dict)
            
            # Extract action steps for this subgoal
            for action in subgoal.get("actionSteps", []):
                action_dict = {
                    "description": action.get("description", action.get("title", "")),
                    "subgoal_index": idx  # Track which subgoal this belongs to
                }
                actions_data.append(action_dict)
        
        return goal_data, subgoals_data, actions_data
    
    def _determine_category(self, index: int, total: int) -> SubgoalCategory:
        """Distribute subgoals across categories."""
        categories = [SubgoalCategory.skill, SubgoalCategory.mental, SubgoalCategory.communication]
        return categories[index % len(categories)]
    
    async def create_goal(self, prompt: str, user_id: int) -> Goal:
        """Create a goal with subgoals and actions based on user prompt."""
        # Get LLM response
        response_text = self.make_llm_request(prompt)
        
        # Parse the response
        goal_data, subgoals_data, actions_data = self.parse_response(response_text)
        
        # Create the main goal
        goal = Goal(
            user_id=user_id,
            title=goal_data["title"],
            description=goal_data["description"],
            status=GoalStatus.active
        )
        goal = await self.goal_repo.create(goal)
        
        # Create subgoals and their actions
        for subgoal_data in subgoals_data:
            subgoal = SubGoal(
                goal_id=goal.id,
                title=subgoal_data["title"],
                description=subgoal_data["description"],
                category=subgoal_data["category"]
            )
            subgoal = await self.subgoal_repo.create(subgoal)
            
            # Create actions for this subgoal
            subgoal_index = subgoals_data.index(subgoal_data)
            related_actions = [a for a in actions_data if a["subgoal_index"] == subgoal_index]
            
            for action_data in related_actions:
                action = Actions(
                    subgoal_id=subgoal.id,
                    description=action_data["description"]
                )
                await self.action_repo.create(action)
        
        return goal
    
    async def delete_goal(self, goal_id: int) -> bool:
        """Delete a goal and all its related subgoals and actions."""
        # Get the goal
        goal = await self.goal_repo.get_by_id(goal_id)
        if not goal:
            return False
        
        await self.goal_repo.delete(goal_id)
        return True
    
    async def get_goal(self, goal_id: int) -> Goal:
        """Retrieve a goal by ID."""
        return await self.goal_repo.get_by_id(goal_id)
    
    async def update_goal_status(self, goal_id: int, status: GoalStatus) -> Goal:
        """Update the status of a goal."""
        goal = await self.goal_repo.get_by_id(goal_id)
        if goal:
            goal.status = status
            await self.db.commit()
            await self.db.refresh(goal)
        return goal
