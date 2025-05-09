import os
import json
import requests
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, Application

# Хендлеры
from handlers.start import handler as start_handler
from handlers.assistant import handler as assistant_handler
from handlers.semantics import handler as semantics_handler
from handlers.serp import handler as serp_handler

# Получаем переменные окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

# Формируем Webhook URL
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}{WEBHOOK_PATH}"

# Инициализируем FastAPI
app = FastAPI()

# Создаём Telegram-приложение
tg_app: Application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Подключаем хендлеры
tg_app.add_handler(start_handler)
tg_app.add_handler(assistant_handler)
tg_app.add_handler(semantics_handler)
tg_app.add_handler(serp_handler)

# При старте сервера — Telegram настраивает Webhook
@app.on_event("startup")
async def on_startup():
    print("📦 TELEGRAM_TOKEN:", TELEGRAM_TOKEN[:10] if TELEGRAM_TOKEN else "❌ None", "...")
    print("🌐 RENDER_EXTERNAL_HOSTNAME:", RENDER_EXTERNAL_HOSTNAME or "❌ None")
    print("🚀 Устанавливаю webhook:", WEBHOOK_URL)

    await tg_app.initialize()
    await tg_app.start()
    await tg_app.bot.set_webhook(url=WEBHOOK_URL)


#  webhook
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    print("🧪 Вход в обработчик /webhook")
    try:
        update_data = await request.json()
        print("📥 Получен JSON:", json.dumps(update_data, indent=2))

        update = Update.de_json(update_data, tg_app.bot)
        await tg_app.update_queue.put(update)

        return {"status": "ok"}
    except Exception as e:
        print("❌ Ошибка при обработке webhook:", str(e))
        return {"status": "error", "message": str(e)}


print("✅ Бот запущен через Webhook")

from fastapi.responses import PlainTextResponse

@app.get("/cache", response_class=PlainTextResponse)
async def list_cache_files():
    try:
        files = os.listdir("serp_cache")
        return "\n".join(files) if files else "📭 Папка serp_cache пуста."
    except Exception as e:
        return f"❌ Ошибка при чтении папки: {e}"

# Обязательный запуск через uvicorn для Render Web Service
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    print(f"🚪 Запускаю Uvicorn на порту {port}...")
    uvicorn.run("bot:app", host="0.0.0.0", port=port)
