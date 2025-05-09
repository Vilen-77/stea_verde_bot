import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Папка для сохранения файлов
SAVE_DIR = "serp_cache"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_meta(url):
    def fetch_meta(url):
        print(f"📄 Получаю мета-данные с: {url}")
    try:
        ...

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""
        description_tag = soup.find("meta", attrs={"name": "description"})
        keywords_tag = soup.find("meta", attrs={"name": "keywords"})
        og_title_tag = soup.find("meta", attrs={"property": "og:title"})
        og_desc_tag = soup.find("meta", attrs={"property": "og:description"})

        description = description_tag["content"].strip() if description_tag and description_tag.has_attr("content") else ""
        keywords = keywords_tag["content"].strip() if keywords_tag and keywords_tag.has_attr("content") else ""
        og_title = og_title_tag["content"].strip() if og_title_tag and og_title_tag.has_attr("content") else ""
        og_desc = og_desc_tag["content"].strip() if og_desc_tag and og_desc_tag.has_attr("content") else ""

        return {
            "url": url,
            "title": title,
            "description": description,
            "keywords": keywords,
            "og_title": og_title,
            "og_description": og_desc
        }

    except Exception as e:
        print(f"❌ Ошибка при получении мета-данных с {url}: {e}")
        return {"url": url, "title": "", "description": "", "keywords": "", "og_title": "", "og_description": ""}

def sanitize_filename(text):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", text)[:50]

def save_raw_meta(user_query, meta_dict):
    def save_raw_meta(user_query, meta_dict):
        print(f"💾 Сохраняю файл для запроса: {user_query}")
        print(f"→ META: {meta_dict}")
    try:
        ...

    try:
        domain = urlparse(meta_dict["url"]).netloc.replace("www.", "")
        main_kw = user_query.split()[0].lower()
        filename = f"{main_kw}-{sanitize_filename(domain)}.txt"
        filepath = os.path.join(SAVE_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            for key, value in meta_dict.items():
                f.write(f"{key.upper()}: {value}\n")

        return filepath
    except Exception as e:
        print(f"❌ Ошибка при сохранении файла: {e}")
        return None
