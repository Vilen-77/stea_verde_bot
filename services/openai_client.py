import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def ask_assistant(user_input: str) -> str:
    prompt = (
        f"Ты — AI-помощник Telegram-бота по ключевикам, SEO и SERP. "
        f"Отвечай дружелюбно, чётко и по теме. Вопрос:\n{user_input}"
    )

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
