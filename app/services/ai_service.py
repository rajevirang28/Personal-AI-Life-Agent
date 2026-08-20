import json
import os

from dotenv import load_dotenv
from ollama import chat


load_dotenv()


OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2"
)


SYSTEM_PROMPT = """
You are a Personal AI Life & Productivity Agent.

You help users with:

- task management
- productivity
- planning
- learning
- goals
- personal organization

Never invent personal information.

Use tools when the user asks for
information that must come from
the user's personal data.
"""
TOOL_SELECTION_PROMPT = """
You are the tool-selection component
of a Personal AI Productivity Agent.

Available tools:

1. get_pending_tasks
   Get all unfinished tasks.

2. get_today_priorities
   Get high-priority unfinished tasks
   due today or overdue.

3. search_memories
   Search personal memories using a keyword.

4. get_task_statistics
   Get the user's task statistics,
   including total, completed, pending,
   and in-progress tasks.

5. get_goals
   Get the user's current goals
   from personal memories.

Rules:

- You may select multiple tools.
- Select only the tools necessary to answer
  the user's question.
- Do not select unrelated tools.
- Return ONLY valid JSON.

Example 1:

User:
"What are my current goals?"

Return:

{
    "use_tools": true,
    "tools": [
        {
            "name": "get_goals",
            "arguments": {}
        }
    ]
}

Example 2:

User:
"What should I work on today?"

Return:

{
    "use_tools": true,
    "tools": [
        {
            "name": "get_today_priorities",
            "arguments": {}
        }
    ]
}

Example 3:

User:
"What are my goals and what should I work on today?"

Return:

{
    "use_tools": true,
    "tools": [
        {
            "name": "get_goals",
            "arguments": {}
        },
        {
            "name": "get_today_priorities",
            "arguments": {}
        }
    ]
}

If no tool is needed:

{
    "use_tools": false,
    "tools": []
}
"""

def choose_tools(
    user_message: str
):

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": TOOL_SELECTION_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    content = (
        response["message"]["content"]
        .strip()
    )

    try:

        return json.loads(content)

    except json.JSONDecodeError:

        return {
            "use_tool": False,
            "tool": None,
            "arguments": {}
        }


def generate_response(
    user_message: str,
    context: str = ""
):

    prompt = f"""
User Context:

{context}

User Message:

{user_message}
"""

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]