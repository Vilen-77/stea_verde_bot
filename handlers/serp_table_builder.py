import os
import csv

# Папка для кэша
CACHE_DIR = "serp_cache"

def generate_serp_table():
    rows = []

    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(".txt"):
            filepath = os.path.join(CACHE_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                url = lines[0].replace("URL:", "").strip() if len(lines) > 0 else ""
                title = lines[1].replace("TITLE:", "").strip() if len(lines) > 1 else ""
                snippet = lines[2].replace("SNIPPET:", "").strip() if len(lines) > 2 else ""
                rows.append({"url": url, "title": title, "snippet": snippet})

    result_path = os.path.join(CACHE_DIR, "result.csv")
    with open(result_path, "w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["url", "title", "snippet"])
        writer.writeheader()
        writer.writerows(rows)

    return result_path

def clear_cache():
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith(".txt"):
            os.remove(os.path.join(CACHE_DIR, filename))
