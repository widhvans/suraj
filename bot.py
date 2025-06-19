# bot.py (Combined Bot and Web App)

import logging
import threading
from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import config

# ==============================================================================
# 1. लॉगिंग और बेसिक कॉन्फ़िगरेशन
# ==============================================================================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("werkzeug").setLevel(logging.WARNING) # Flask के सर्वर लॉग्स को शांत करने के लिए
logger = logging.getLogger(__name__)


# ==============================================================================
# 2. वेबसाइट (FLASK APP) का हिस्सा
# ==============================================================================

# Flask ऐप ऑब्जेक्ट बनाएं
# template_folder='templates' यह सुनिश्चित करता है कि Flask सही जगह पर HTML फाइल ढूंढे
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    """वेबसाइट का मुख्य पेज रेंडर करता है।"""
    try:
        # index.html फाइल को रेंडर (प्रदर्शित) करें
        return render_template('index.html', channel_link=config.STUDY_CHANNEL_LINK)
    except Exception as e:
        logger.error(f"Template rendering error: {e}")
        return "Internal Server Error: Could not render template. Please check logs.", 500

def run_flask_app():
    """Flask वेब सर्वर को चलाने वाला फंक्शन।"""
    logger.info(f"Starting Flask web server on http://{config.VPS_IP}:{config.PORT}")
    # host='0.0.0.0' का मतलब है कि यह सर्वर सभी पब्लिक IP पर उपलब्ध होगा
    app.run(host='0.0.0.0', port=config.PORT, debug=False)


# ==============================================================================
# 3. टेलीग्राम बॉट का हिस्सा
# ==============================================================================

async def send_website_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """यूजर को वेबसाइट का लिंक भेजता है।"""
    keyboard = [
        [InlineKeyboardButton("🌐 हमारी वेबसाइट पर जाएं", url=config.WEBSITE_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = (
        "नमस्ते! 👋\n\n"
        "हमारी सेवाओं और सब्सक्रिप्शन प्लान की पूरी जानकारी के लिए, कृपया हमारी वेबसाइट पर जाएं।\n\n"
        f"आप सीधे इस लिंक पर भी क्लिक कर सकते हैं: {config.WEBSITE_URL}"
    )
    await update.message.reply_text(message_text, reply_markup=reply_markup)

async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """किसी भी टेक्स्ट मैसेज का जवाब देता है।"""
    logger.info(f"Received message from {update.effective_user.first_name}")
    await send_website_link(update, context)


# ==============================================================================
# 4. मुख्य फंक्शन (सब कुछ शुरू करने के लिए)
# ==============================================================================

def main() -> None:
    """वेबसाइट और बॉट दोनों को शुरू करता है।"""
    
    # --- वेबसाइट को एक अलग थ्रेड में शुरू करें ---
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True  # यह सुनिश्चित करता है कि बॉट बंद होने पर थ्रेड भी बंद हो जाए
    flask_thread.start()
    
    # --- टेलीग्राम बॉट को मुख्य थ्रेड में शुरू करें ---
    application = Application.builder().token(config.BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", send_website_link))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))

    logger.info("Starting Telegram bot polling...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
