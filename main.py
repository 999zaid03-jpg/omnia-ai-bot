import os
import logging
import asyncio
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

# Render ရဲ့ Environment Variables ကနေပဲ အသေအချာဖတ်ခိုင်းမယ်
TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_KEY")

# Gemini API ပြင်ဆင်ခြင်း
genai.configure(api_key=GEMINI_KEY)

# ဗားရှင်းဟောင်းတွေမှာပါ အလုပ်လုပ်အောင် မော်ဒယ်နာမည်ကို 'gemini-pro' လို့ ပြောင်းသုံးကြည့်ပါမယ်
try:
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        system_instruction="You are OmniaCapital AI, a professional assistant for OmniaCapital Group. Answer user questions in a helpful and polite manner in both English and Burmese. Focus on financial and investment topics related to the group."
    )
except Exception:
    # အကယ်၍ system_instruction နဲ့ မကိုက်ညီရင် ရိုးရိုးပဲ ဆောက်မယ်
    model = genai.GenerativeModel(model_name="gemini-pro")

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
