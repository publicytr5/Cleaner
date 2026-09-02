import os
import logging
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# লগিং সেটিং
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Render Keep-Alive এর জন্য Flask Server
app = Flask('')

@app.route('/')
def home():
    return "Bot is running fine!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# স্টার্ট কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("হ্যালো! আমি গ্রুপ থেকে জয়েন ও লিভ মেসেজ ডিলিট করার বট। আমাকে গ্রুপে এডমিন করুন।")

# জয়েন ও লিভ মেসেজ ডিলিট করার ফাংশন
async def delete_service_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except Exception as e:
        logging.error(f"Error deleting message: {e}")

def main():
    # Environment Variable থেকে টোকেন সংগ্রহ
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN Environment Variable পাওয়া যায়নি!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    # হ্যান্ডলার এড করা
    application.add_handler(CommandHandler("start", start))
    
    # Status Update (Join/Leave) ফিল্টার
    application.add_handler(MessageHandler(filters.StatusUpdate.ALL, delete_service_messages))

    # Flask সার্ভার চালু করা (UptimeRobot এর জন্য)
    keep_alive()

    # বট স্টার্ট
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
