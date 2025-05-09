import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Папка для сохранения файлов
SAVE_DIR = "serp_cache"
os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_meta(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        title = soup.title.string.strip() if soup.title else ""
        description = soup.find("meta", attrs={"name": "description"})
        description = description["content"].strip() if description and description.has_attr("content") else ""
        keywords = soup.find("meta", attrs={"name": "keywords"})
        keywords = keywords["content"].strip() if keywords and keywords.has_attr("content") else ""

        return title, description, keywords

    except Exception as e:
        print(f"❌ Ошибка при получении мета-данных с {url}: {e}")
        return "", "", ""

def extract_keywords(text):
    words = re.findall(r"\b[\w\-]{3,}\b", text.lower())
    return sorted(set(words))

def sanitize_filename(text):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", text)[:50]

def save_to_file(user_query, url, keywords):
    try:
        domain = urlparse(url).netloc.replace("www.", "")
        main_kw = user_query.split()[0].lower()
        filename = f"{main_kw}-{sanitize_filename(domain)}.txt"
        filepath = os.path.join(SAVE_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"URL: {url}\n")
            for kw in keywords:
                f.write(f"{kw}\n")

        return filepath
    except Exception as e:
        print(f"❌ Ошибка при сохранении файла: {e}")
        return None
