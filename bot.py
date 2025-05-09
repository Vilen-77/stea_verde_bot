import os
import json
import requests
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import ApplicationBuilder, Application

# Хендлеры
from handlers.start import handler as start_handler
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
tg_app.add_handler(assistant_handler)

# При старте сервера — Telegram настраивает Webhook
@app.on_event("startup")
async def on_startup():
    print("📦 TELEGRAM_TOKEN:", TELEGRAM_TOKEN[:10] if TELEGRAM_TOKEN else "❌ None", "...")
    print("🌐 RENDER_EXTERNAL_HOSTNAME:", RENDER_EXTERNAL_HOSTNAME or "❌ None")
    print("🚀 Устанавливаю webhook:", WEBHOOK_URL)
    await tg_app.bot.set_webhook(url=WEBHOOK_URL)

# Упрощённый webhook для отладки
@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    print("🧪 Вход в обработчик /webhook")
    try:
        body = await request.body()
        print("📥 Пришёл raw webhook (байты):", body[:300])
        return {"status": "ok"}
    except Exception as e:
        print("❌ Ошибка чтения webhook:", str(e))
        return {"status": "error", "message": str(e)}

print("✅ Бот запущен через Webhook")

# Обязательный запуск через uvicorn для Render Web Service
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    print(f"🚪 Запускаю Uvicorn на порту {port}...")
    uvicorn.run("bot:app", host="0.0.0.0", port=port)
