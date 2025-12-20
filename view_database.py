"""View Apollo database contents"""
import psycopg2
from psycopg2.extras import RealDictCursor

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="postgres",
    password="1234",
    database="apollo"
)

cursor = conn.cursor(cursor_factory=RealDictCursor)

print("=" * 80)
print("APOLLO DATABASE CONTENTS")
print("=" * 80)

# Users
print("\n📊 USERS TABLE:")
print("-" * 80)
cursor.execute("SELECT id, user_name, email, created_at FROM users ORDER BY id")
users = cursor.fetchall()
if users:
    for user in users:
        print(f"ID: {user['id']} | Username: {user['user_name']} | Email: {user['email']}")
        print(f"   Created: {user['created_at']}")
else:
    print("(empty)")

# Goals
print("\n🎯 GOALS TABLE:")
print("-" * 80)
cursor.execute("SELECT id, user_id, title, description, status, created_at FROM goals ORDER BY id")
goals = cursor.fetchall()
if goals:
    for goal in goals:
        print(f"\nGoal #{goal['id']} (User: {goal['user_id']}) - Status: {goal['status']}")
        print(f"Title: {goal['title']}")
        print(f"Description: {goal['description'][:100]}...")

        # Get subgoals for this goal
        cursor.execute(
            "SELECT id, title, description, category FROM subgoals WHERE goal_id = %s ORDER BY id",
            (goal['id'],)
        )
        subgoals = cursor.fetchall()

        if subgoals:
            print(f"\n  📌 Sub-goals ({len(subgoals)}):")
            for idx, subgoal in enumerate(subgoals, 1):
                print(f"    {idx}. [{subgoal['category']}] {subgoal['title']}")

                # Get actions for this subgoal
                cursor.execute(
                    "SELECT id, description FROM actions WHERE subgoal_id = %s ORDER BY id",
                    (subgoal['id'],)
                )
                actions = cursor.fetchall()

                if actions:
                    print(f"       Actions ({len(actions)}):")
                    for action_idx, action in enumerate(actions, 1):
                        desc = action['description'][:70] if action['description'] else "N/A"
                        print(f"         {action_idx}. {desc}")
else:
    print("(empty)")

# Summary counts
print("\n" + "=" * 80)
print("SUMMARY:")
print("-" * 80)
cursor.execute("SELECT COUNT(*) as count FROM users")
user_count = cursor.fetchone()['count']
cursor.execute("SELECT COUNT(*) as count FROM goals")
goal_count = cursor.fetchone()['count']
cursor.execute("SELECT COUNT(*) as count FROM subgoals")
subgoal_count = cursor.fetchone()['count']
cursor.execute("SELECT COUNT(*) as count FROM actions")
action_count = cursor.fetchone()['count']

print(f"Total Users: {user_count}")
print(f"Total Goals: {goal_count}")
print(f"Total Sub-goals: {subgoal_count}")
print(f"Total Actions: {action_count}")
print("=" * 80)

cursor.close()
conn.close()
