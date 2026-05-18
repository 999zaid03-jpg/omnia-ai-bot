import os
import logging
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# --- Render Web Server ---
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
# -------------------------

TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Gemini Standard Configuration
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="You are OmniaCapital AI, a professional assistant for OmniaCapital Group. Answer user questions in a helpful and polite manner in both English and Burmese. Focus on financial and investment topics related to the group."
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("OmniaCapital Group မှ ကြိုဆိုပါတယ်။ ကျွန်တော်က AI Assistant ပါဗျာ။ ဘာများ ကူညီပေးရမလဲခင်ဗျာ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = model.generate_content(update.message.text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error handling message: {e}")
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
