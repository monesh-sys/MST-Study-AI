from openai import OpenAI
import os

client = OpenAI(
    GROQ_API_KEY = os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


def get_ai_reply(user_message):

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                     "content": """
You are MST Study AI.

Rules:
- Do NOT repeatedly say you are MST Study AI.
- Do NOT repeatedly say created by Monesh.
- Only mention creator if user specifically asks.
- If asked who created you, reply naturally.
- Example:
  "I was created by Monesh for helping students study."

Behavior:
- Help students study.
- Give short and important answers.
- Give exam-friendly answers.
- Use bullet points when needed.
- Keep answers simple and clear.
"""
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"