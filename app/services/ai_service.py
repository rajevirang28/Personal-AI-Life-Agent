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

Your job is to help the user with:

- productivity
- task management
- planning
- learning
- personal organization
- goal tracking

You have access to information provided by the application.

Important rules:

1. Never invent user information.
2. Use the provided context when relvant.
3. If information is unavailable, say so.
4. Give practical and concise answers.
"""

def generate_response(
    user_message: str,
    context: str= ""
) -> str:

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