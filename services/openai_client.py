import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Загружаем системный prompt из текстового файла
def load_prompt_template():
    with open("prompt_templates/assistant_prompt.txt", "r", encoding="utf-8") as f:
        return f.read()

# AI-помощник
async def ask_assistant(user_input: str) -> str:
    system_prompt = load_prompt_template()
    full_prompt = f"{system_prompt}\n\nВопрос:\n{user_input}"

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": full_prompt}]
    )
    return response.choices[0].message.content.strip()
