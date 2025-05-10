# bot.py — Telegram-бот с Webhook через FastAPI (для Render Web Service)

import os
from fastapi import FastAPI, Request
from telegram import Update
from telegram.ext import Application, ApplicationBuilder
from telegram.ext import CommandHandler, ContextTypes
from telegram.constants import ChatAction
from modules.upload_to_drive import upload_to_drive
from modules.get_log_file import getlog
from modules.ai_assistant import ask_ai

# Настройки окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
RENDER_EXTERNAL_HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = f"https://{RENDER_EXTERNAL_HOSTNAME}{WEBHOOK_PATH}"

# Telegram Application
tg_app: Application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

# Регистрация команд
ADMIN_USERNAME = "Vilen77"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.username

    if username == ADMIN_USERNAME:
        await update.message.reply_text("Привет, админ! Бот работает.")
    else:
        await update.message.reply_text("Здравствуйте! Я виртуальный помощник. Чем могу помочь?")
        try:
            upload_to_drive("log_stea_verde.txt")
        except Exception as e:
            print("Ошибка при загрузке лога:", e)

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(CommandHandler("getlog", getlog))
tg_app.add_handler(CommandHandler("ask", ask_ai))

# FastAPI
app = FastAPI()

@app.on_event("startup")
async def on_startup():
    print("🚀 Запуск Telegram Webhook:", WEBHOOK_URL)
    await tg_app.initialize()
    await tg_app.start()
    await tg_app.bot.set_webhook(url=WEBHOOK_URL)

@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    try:
        update_data = await request.json()
        update = Update.de_json(update_data, tg_app.bot)
        await tg_app.update_queue.put(update)
        return {"status": "ok"}
    except Exception as e:
        print("❌ Ошибка обработки webhook:", e)
        return {"status": "error", "message": str(e)}

# Запуск с uvicorn
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("bot:app", host="0.0.0.0", port=port)
