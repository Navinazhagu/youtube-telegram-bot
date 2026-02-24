import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters
from telegram_handler import handle_message

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot is running...")
app.run_polling()