import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ============================================
# التوكنات المزودة (تم إدخالها مباشرة)
# ============================================
TELEGRAM_TOKEN = "8626096117:AAHARMDbGYCp4d9y9GKCV5qduVrNKrqSxK0"
NVIDIA_API_KEY = "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"
# ============================================

INVOKE_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ بوت NVIDIA AI يعمل.\nأرسل أي نص وسأرد عليه.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    
    headers = {
        "Authorization": f"Bearer {NVIDIA_API_KEY}",
        "Accept": "application/json"
    }
    
    payload = {
        "model": "mistralai/mistral-medium-3.5-128b",
        "messages": [{"role": "user", "content": user_message}],
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 1.0,
        "stream": False
    }
    
    try:
        response = requests.post(INVOKE_URL, headers=headers, json=payload)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
        else:
            reply = f"❌ خطأ API: {response.status_code}\n{response.text}"
    except Exception as e:
        reply = f"❌ خطأ: {str(e)}"
    
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    print("🚀 البوت يعمل...")
    main()
