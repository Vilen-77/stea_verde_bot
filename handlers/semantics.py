from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import os
from openai import OpenAI

# Инициализация клиента OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Загрузка шаблона prompt из файла
PROMPT_TEMPLATE_PATH = "prompt_templates/prompt_semantics.txt"
if os.path.exists(PROMPT_TEMPLATE_PATH):
    with open(PROMPT_TEMPLATE_PATH, "r", encoding="utf-8") as f:
        PROMPT_TEMPLATE = f.read()
else:
    PROMPT_TEMPLATE = "Сгенерируй список из 30 ключевых фраз по теме '{query}', раздели их по интенту (информационные, коммерческие, транзакционные) и оформи списком."

# Основная логика команды /semantics
async def semantics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Пожалуйста, укажи тему после /semantics.")
        return

    prompt = PROMPT_TEMPLATE.replace("{query}", query)

    await update.message.reply_text(f"✍️ Генерирую ключевые фразы по теме: {query}...")

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()
        await update.message.reply_text(result)

    except Exception as e:
        print("❌ Ошибка OpenAI:", e)
        await update.message.reply_text("Произошла ошибка при запросе к OpenAI. Попробуйте позже.")

# Хендлер команды
handler = CommandHandler("semantics", semantics_command)
