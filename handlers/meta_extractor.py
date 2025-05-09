import os
import re
from urllib.parse import urlparse

# Папка для сохранения файлов
SAVE_DIR = "serp_cache"
os.makedirs(SAVE_DIR, exist_ok=True)

def sanitize_filename(text):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", text)[:80]

def save_raw_meta_from_serp(user_query, url, title, snippet):
    print(f"💾 Сохраняю файл для: {url}")
    try:
        domain = urlparse(url).netloc.replace("www.", "")
        main_kw = sanitize_filename(user_query.lower().replace(" ", "-"))
        filename = f"{main_kw}-{sanitize_filename(domain)}.txt"
        filepath = os.path.join(SAVE_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n")
            f.write(f"TITLE: {title}\n")
            f.write(f"SNIPPET: {snippet}\n")

        print(f"✅ Файл реально сохранён по пути: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Ошибка при сохранении файла: {e}")
        return None
