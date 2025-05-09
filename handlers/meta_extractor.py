import os
import re
from urllib.parse import urlparse

# Папка для сохранения файлов
SAVE_DIR = "serp_cache"
os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(text):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", text)[:50]

def save_raw_meta_from_serp(user_query, link, serp_title, serp_snippet):
    print(f"💾 Сохраняю файл для: {link}")
    try:
        domain = urlparse(link).netloc.replace("www.", "")
        main_kw = sanitize_filename(user_query.lower().replace(" ", "-"))
        filename = f"{main_kw}-{sanitize_filename(domain)}.txt"
        filepath = os.path.join(SAVE_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {link}\n")
            f.write(f"TITLE: {serp_title}\n")
            f.write(f"SNIPPET: {serp_snippet}\n")

        print(f"✅ Файл сохранён: {filepath}")
        return filepath

    except Exception as e:
        print(f"❌ Ошибка при сохранении мета-данных: {e}")
        return None
