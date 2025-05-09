from telegram import Update
from telegram.ext import MessageHandler, ContextTypes, filters
from services.openai_client import ask_assistant  # создадим позже

async def assistant_handler_fn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = await ask_assistant(user_text)
    await update.message.reply_text(reply)

handler = MessageHandler(filters.TEXT & ~filters.COMMAND, assistant_handler_fn)
