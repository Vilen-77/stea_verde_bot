from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import os
import requests
from handlers.meta_extractor import save_raw_meta_from_serp

# Получаем ключ из переменных окружения
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Разбор аргументов команды: +N, L, R
def parse_serp_args(args):
    query_parts = []
    count = 10  # по умолчанию
    lang = "ro"
    region = "ro"

    for arg in args:
        if arg.startswith('+') and arg[1:].isdigit():
            count += int(arg[1:])
        elif arg.lower().startswith('l='):
            lang = arg[2:]
        elif arg.lower().startswith('r='):
            region = arg[2:]
        else:
            query_parts.append(arg)

    return ' '.join(query_parts), count, lang, region

# Команда /serp
async def serp_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Пожалуйста, укажите поисковый запрос после /serp")
        return

    query, count, lang, region = parse_serp_args(context.args)
    await update.message.reply_text(f"🔍 Ищу: *{query}*\n🌐 Язык: {lang}, Регион: {region}\n📦 Результатов: {count}", parse_mode="Markdown")

    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "hl": lang,
        "gl": region
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()
        results = data.get("organic_results", [])[:count]

        if not results:
            await update.message.reply_text("❌ Результаты не найдены.")
            return

        message = "📄 *Топ результатов:*\n\n"
        
       


        for idx, res in enumerate(results, start=1):
            title = res.get("title", f"Результат {idx}")
            link = res.get("link", "")
            message += f"• [{title}]({link})\n"
            
            print(f"🌐 Парсю ссылку: {link}")
            meta = fetch_meta(link)
            print(f"🧠 META: {meta}")
            save_raw_meta(query, meta)
  

            # Извлекаем и сохраняем мета-данные без обработки
            from handlers.meta_extractor import save_raw_meta_from_serp

            title = res.get("title", "")
            snippet = res.get("snippet", "")
            save_raw_meta_from_serp(query, link, title, snippet)


        await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        print("❌ Ошибка запроса к SerpAPI:", e)
        await update.message.reply_text("⚠️ Не удалось получить результаты из SerpAPI.")

# Хендлер команды
handler = CommandHandler("serp", serp_command)
