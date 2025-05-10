import os
from datetime import datetime

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
            allowed = [line.strip() for line in f]
        return username in allowed
    except Exception as e:
        print(f"❌ Ошибка при проверке прав пользователя: {e}")
        return False
