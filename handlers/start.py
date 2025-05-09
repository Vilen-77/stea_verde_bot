from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я — Semantica Bot 🤖. Напиши /semantics <тема>, чтобы сгенерировать ключевые фразы."
    )

handler = CommandHandler("start", start_command)
