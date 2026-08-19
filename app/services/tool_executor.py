from sqlalchemy.orm import Session

from app.tools.registry import TOOLS

def execute_tool(
        tool_name: str,
        arguments: dict,
        db: Session,
        user_id: int
):
    if tool_name not in TOOLS:
        raise ValueError(
            f"Unknown tool: {tool_name}"
        )
    
    tool = TOOLS[tool_name]

    return tool(
        db=db,
        user_id=user_id,
        **arguments
    )