from app.database.database import SessionLocal
from app.tools.task_tools import create_task


db = SessionLocal()

try:
    result = create_task(
        db=db,
        user_id=1,
        title="Learn Agentic AI",
        description="Study tool calling and agent workflows",
        priority="high"
    )

    print(result)

finally:
    db.close()