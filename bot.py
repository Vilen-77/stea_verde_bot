import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from openai import OpenAI

# Загрузка переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Инициализация OpenAI клиента
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я stea_verde_bot 🤖. Напиши /semantics <тема>, и я сгенерирую семантическое ядро.")

# Команда /semantics <запрос>
async def semantics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Пожалуйста, укажи ключевую фразу после /semantics.")
        return

    prompt = f"Сгенерируй список из 30 ключевых фраз по теме '{query}', раздели их по интенту (информационные, коммерческие, транзакционные) и оформи списком."

    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content.strip()
        await update.message.reply_text(result)

    except Exception as e:
        await update.message.reply_text(f"Ошибка: {str(e)}")
        import os
import requests
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Получаем ключ SerpApi из переменных
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

async def serp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    if not query:
        await update.message.reply_text("Пожалуйста, укажи запрос после /serp")
        return

    await update.message.reply_text(f"🔎 Ищу результаты в Google по: *{query}* ...", parse_mode="Markdown")

    # Запрос к SerpApi
    params = {
        "engine": "google",
        "q": query,
        "hl": "ro",   # Язык интерфейса
        "gl": "ro",   # Гео (Румыния)
        "api_key": SERPAPI_KEY
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        if "organic_results" not in data:
            await update.message.reply_text("❌ Не удалось получить результаты.")
            return

        results = data["organic_results"][:5]  # топ-5

        message = "📄 *Топ-результаты Google:*\n\n"
        for res in results:
            title = res.get("title", "Без заголовка")
            link = res.get("link", "")
            message += f"• [{title}]({link})\n"

        await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при запросе: {e}")


# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("semantics", semantics))
    app.add_handler(CommandHandler("serp", serp))
    app.run_polling()

if __name__ == "__main__":
    main()
