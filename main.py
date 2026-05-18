import os
import logging
import asyncio
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# --- Render Web Server (Port Open) ---
flask_app = Flask('')

@flask_app.route('/')
def home():
    return "OmniaCapital Bot Is Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    flask_app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()
# -------------------------------------

# Environment Variables ကနေ တိုက်ရိုက်ဖတ်မယ်
TOKEN = os.getenv("TELEGRAM_TOKEN", "8980631594:AAFwxbnJtA3HYGEiVVwSy--nWOx1NZD3usw")
GEMINI_KEY = os.getenv("GEMINI_KEY", "AIzaSyCmUzL-uTfv7Q3b66I-F9O0hsNC4toE7ZY")

# Gemini Setup (Unicode စနစ်မှန်ဖြင့် ပြင်ဆင်ထားသည်)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are OmniaCapital AI, a professional assistant for OmniaCapital Group. Answer user questions in a helpful and polite manner in both English and Burmese. Focus on financial and investment topics related to the group."
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # စာသားကို ယူနီကုတ် စနစ်အမှန်ဖြင့် ပြန်ပြင်ထားပါတယ်
    await update.message.reply_text("OmniaCapital Group မှ ကြိုဆိုပါတယ်။ ကျွန်တော်က AI Assistant ပါဗျာ။ ဘာများ ကူညီပေးရမလဲခင်ဗျာ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # AI ထံမှ အဖြေတောင်းခြင်း
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        # တကယ့် Error အစစ်ကိုပါ Bot ထဲမှာ လှမ်းပြခိုင်းလိုက်မယ် (ရှာရလွယ်အောင်)
        await update.message.reply_text(f"စနစ်ပိုင်းဆိုင်ရာ ချို့ယွင်းချက်ရှိနေပါသည်။\nError: {e}")

def main():
    keep_alive()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logging.info("Starting bot polling...")
    app.run_polling()

if __name__ == "__main__":
    main()
