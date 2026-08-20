from sqlalchemy.orm import Session

from app.services.ai_service import (
    choose_tools,
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

    decision = choose_tools(
        user_message
    )

    print(
        "\n[AGENT] Tool decision:"
    )

    print(decision)

    if not decision.get(
        "use_tools",
        False
    ):

        return generate_response(
            user_message=user_message
        )

    selected_tools = decision.get(
        "tools",
        []
    )

    if not selected_tools:

        return generate_response(
            user_message=user_message
        )

    tool_results = []

    for selected_tool in selected_tools:

        tool_name = selected_tool.get(
            "name"
        )

        arguments = selected_tool.get(
            "arguments",
            {}
        )

        print(
            f"[AGENT] Executing tool: "
            f"{tool_name}"
        )

        try:

            result = execute_tool(
                tool_name=tool_name,
                arguments=arguments,
                db=db,
                user_id=user_id
            )

            formatted_result = (
                format_tool_result(
                    tool_name=tool_name,
                    result=result
                )
            )

            tool_results.append(
                f"""
                TOOL: {tool_name}

                RESULT:

                {formatted_result}
                """
            )

        except Exception as e:

            tool_results.append(
                f"""
                TOOL: {tool_name}

                ERROR:

                {str(e)}
                """
            )

    combined_results = "\n".join(
        tool_results
    )

    print(
        "[AGENT] Tool results:"
    )

    print(combined_results)

    final_prompt = f"""
You are a Personal AI Life
and Productivity Agent.

The user asked:

{user_message}

The following tools were executed:

{combined_results}

Use the tool results to answer
the user's question.

Rules:

1. Do not invent information.
2. Only use information from the
   tool results when discussing
   the user's personal data.
3. If multiple tools returned information,
   combine them into one useful answer.
4. Be concise and practical.
"""

    return generate_response(
        user_message=final_prompt
    )