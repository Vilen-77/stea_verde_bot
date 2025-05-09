import os
import json
import requests
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, Application

# Хендлеры
from handlers.start import handler as start_handler
# from handlers.semantics import handler as semantics_handler
# from handlers.serp_fetch import handler as serp_handler
# from handlers.stats import handler as stats_handler
# from handlers.admin import handler as admin_handler
from handlers.assistant import handler as assistant_handler

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
# tg_app.add_handler(semantics_handler)
# tg_app.add_handler(serp_handler)
# tg_app.add_handler(stats_handler)
# tg_app.add_handler(admin_handler)
tg_app.add_handler(assistant_handler)

# При старте сервера — Telegram настраивает Webhook
@app.on_event("startup")
async def on_startup():
    print("🚀 Устанавливаю webhook:", WEBHOOK_URL)
    await tg_app.bot.set_webhook(url=WEBHOOK_URL)

# Обработка входящих сообщений от Telegram
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    print("🧪 Вызван обработчик /webhook")
    try:
        update_data = await request.json()
        print("📥 Получен webhook от Telegram!")
        print(json.dumps(update_data, indent=2))

        update = Update.de_json(update_data, tg_app.bot)
        await tg_app.update_queue.put(update)

        return {"status": "ok"}
    except Exception as e:
        print("❌ Ошибка при обработке webhook:", str(e))
        return {"status": "error", "message": str(e)}

print("✅ Бот запущен через Webhook")
