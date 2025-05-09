async def serp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    base_count = 5
    max_count = 20
    extra_count = 0
    query_parts = []

    for arg in args:
        if arg.startswith('+') and arg[1:].isdigit():
            extra_count += int(arg[1:])
        else:
            query_parts.append(arg)

    total_count = min(base_count + extra_count, max_count)
    query = ' '.join(query_parts).strip()

    if not query:
        await update.message.reply_text("Пожалуйста, укажи запрос после /serp")
        return

    await update.message.reply_text(f"🔎 Ищу результаты в Google по: *{query}* ...", parse_mode="Markdown")

    # Запрос к SerpApi
    params = {
        "engine": "google",
        "q": query,
        "hl": "ro",
        "gl": "ro",
        "api_key": SERPAPI_KEY
    }

    try:
        response = requests.get("https://serpapi.com/search", params=params)
        data = response.json()

        if "organic_results" not in data:
            await update.message.reply_text("❌ Не удалось получить результаты.")
            return

        results = data["organic_results"][:total_count]

        message = f"📄 *Топ-{len(results)} результатов Google:*\n\n"
        for res in results:
            title = res.get("title", "Без заголовка")
            link = res.get("link", "")
            message += f"• [{title}]({link})\n"

        await update.message.reply_text(message, parse_mode="Markdown", disable_web_page_preview=True)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Ошибка при запросе: {e}")
