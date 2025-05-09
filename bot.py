from telegram.ext import ApplicationBuilder
#from handlers.start import handler as start_handler
#from handlers.semantics import handler as semantics_handler
#from handlers.serp_fetch import handler as serp_handler
#from handlers.stats import handler as stats_handler
#from handlers.admin import handler as admin_handler
#from handlers.assistant import handler as assistant_handler

import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    #app.add_handler(start_handler)
    #app.add_handler(semantics_handler)
    #app.add_handler(serp_handler)
    #app.add_handler(stats_handler)
    #app.add_handler(admin_handler)
    #app.add_handler(assistant_handler)

    print("✅ Бот запущен. Ожидаю команды в Telegram...")
    app.run_polling(stop_signals=None)
