from sqlalchemy.orm import Session

from app.services.ai_service import (
    choose_tool,
    generate_response
)

from app.services.tool_executor import (
    execute_tool
)

from app.services.tool_formatter import (
    format_tool_result
)


def run_agent(
    db: Session,
    user_id: int,
    user_message: str
):

    decision = choose_tool(
        user_message
    )

    if not decision.get(
        "use_tool",
        False
    ):

        return generate_response(
            user_message=user_message
        )

    tool_name = decision.get(
        "tool"
    )

    arguments = decision.get(
        "arguments",
        {}
    )

    try:

        result = execute_tool(
            tool_name=tool_name,
            arguments=arguments,
            db=db,
            user_id=user_id
        )

    except Exception as e:

        return (
            "I couldn't access that "
            f"information right now: {str(e)}"
        )
    
    tool_result = format_tool_result(
        tool_name=tool_name,
        result=result
    )

    final_context = f"""
The user asked:

{user_message}

You used the tool:

{tool_name}

The tool returned:

{tool_result}

Use this information to answer
the user's question.

Do not invent information.
"""

    return generate_response(
        user_message=final_context
    )