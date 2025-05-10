from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from utils.user_name import log_user_info

#async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
#   await update.message.reply_text(
#        "Привет! Я — Semantica Bot 🤖. Обладаю искусственным интелектом и имею спецпропуск в секретную базу Google! Собран офигенным парнем с румынского села) Умею работать с ключевыми фразами, давать короткие справки по SEO. Если нужен список команд, спросите меня)"
#    )
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    log_user_info(user.id, user.username)  # ⬅️ логируем пользователя

    await update.message.reply_text(
        "Привет! Я — Semantica Bot 🤖. Напиши /semantics <тема>, чтобы сгенерировать ключевые фразы."
    )

handler = CommandHandler("start", start_command)
