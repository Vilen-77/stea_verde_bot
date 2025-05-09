from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я — Semantica Bot 🤖. Обладаю искусственным интелектом и имею спецпропуск в секретную базу Google! Собран офигенным парнем с румынского села) Умею работать с ключевыми фразами, давать короткие справки по SEO. Если нужен список команд, спросите меня)"
    )

handler = CommandHandler("start", start_command)
