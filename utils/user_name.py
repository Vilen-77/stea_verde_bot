import os
from datetime import datetime
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

# Файл для логирования пользователей
LOG_FILE = "user_logs.txt"
# Файл со списком разрешённых пользователей
ALLOWED_USERS_FILE = "allowed_users.txt"


def log_user_info(user_id: int, username: str):
    """
    Логирует информацию о пользователе в файл с отметкой времени
    """
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} - ID: {user_id} - Username: {username}\n")
    except Exception as e:
        print(f"❌ Ошибка логирования пользователя: {e}")


def is_user_allowed(username: str) -> bool:
    """
    Проверяет, есть ли имя пользователя в списке разрешённых
    """
    if username == "Vilen77":  # безусловный доступ владельцу
        return True

    if not os.path.exists(ALLOWED_USERS_FILE):
        return False

    try:
        with open(ALLOWED_USERS_FILE, "r", encoding="utf-8") as f:
            allowed = [line.strip() for line in f if line.strip()]
        return username in allowed
    except Exception as e:
        print(f"❌ Ошибка при проверке прав пользователя: {e}")
        return False


async def download_log_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Команда /getlog — отправка файла с логами (только для Vilen77)
    """
    user = update.effective_user
    if user.username != "Vilen77":
        await update.message.reply_text("⛔ У Вас нет прав для этой команды.")
        return

    if not os.path.exists(LOG_FILE):
        await update.message.reply_text("📭 Лог-файл пока пуст или отсутствует.")
        return

    await update.message.reply_document(document=open(LOG_FILE, "rb"), filename="user_logs.txt")


# Хендлер команды /getlog
getlog_handler = CommandHandler("getlog", download_log_command)
