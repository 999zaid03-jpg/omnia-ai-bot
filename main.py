import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# --- Render Web Server (Timeout မဖြစ်အောင်) ---
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "OmniaCapital Bot Is Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()
# ---------------------------------------------

# Configuration
TOKEN = os.getenv("TELEGRAM_TOKEN", "8980631594:AAFwxbnJtA3HYGEiVVwSy--nWOx1NZD3usw")
GEMINI_KEY = os.getenv("GEMINI_KEY", "AIzaSyCmUzL-uTfv7Q3b66I-F9O0hsNC4toE7ZY")

# AI Setup (ဗားရှင်းဟောင်းပုံစံ ပြင်ထားပါတယ်)
genai.configure(api_key=GEMINI_KEY)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("OmniaCapital Group မှ ကြိုဆိုပါတယ်။ ကျွန်တော်က AI assistant ပါ။ ဘာများ ကူညီပေးရမလဲခင်ဗျာ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # ဗားရှင်းဟောင်းအတွက် code အလုပ်လုပ်ပုံ ပြောင်းထားပါတယ်
        response = genai.generate_text(
            model="models/gemini-1.5-flash",
            prompt=f"System Instruction: You are OmniaCapital AI, a professional assistant for OmniaCapital Group. Answer user questions in a helpful and polite manner in both English and Burmese. Focus on financial and investment topics related to the group.\n\nUser: {update.message.text}"
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        await update.message.reply_text("ခေတ္တဆိုင်းငံ့ထားပါ၊ ခဏနေမှ ပြန်မေးပေးပါခင်ဗျာ။")

def main():
    keep_alive()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
