import logging
import html
import json
import traceback
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
logging.getLogger("werkzeug").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# ==============================================================================
# 2. वेबसाइट (FLASK APP) का हिस्सा (कोई बदलाव नहीं)
# ==============================================================================
app = Flask(__name__, template_folder='templates')
@app.route('/')
def index():
    return render_template('index.html')
def run_flask_app():
    logger.info(f"Starting Flask web server on http://{config.VPS_IP}:{config.PORT}")
    app.run(host='0.0.0.0', port=config.PORT, debug=False)

# ==============================================================================
# 3. टेलीग्राम बॉट का हिस्सा (सुधार के साथ)
# ==============================================================================

# ---> नया: एरर हैंडलर फंक्शन <---
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """किसी भी एरर को लॉग करता है।"""
    logger.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    logger.error(f"Traceback: {tb_string}")


async def send_website_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """यूजर को वेबसाइट का लिंक भेजता है।"""
    keyboard = [[InlineKeyboardButton("🌐 हमारी वेबसाइट पर जाएं", url=config.WEBSITE_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message_text = (
        "नमस्ते! 👋\n\n"
        f"हमारी सेवाओं की जानकारी के लिए, कृपया हमारी वेबसाइट पर जाएं: {config.WEBSITE_URL}"
    )
    if update.message:
        await update.message.reply_text(message_text, reply_markup=reply_markup)

# ---> सुधारित: handle_any_message फंक्शन <---
async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """किसी भी टेक्स्ट मैसेज का जवाब देता है और सुरक्षित रूप से लॉग करता है।"""
    
    # यह जांच एरर को रोक देगी
    user = update.effective_user
    if user:
        logger.info(f"Received message from {user.first_name} (ID: {user.id})")
    else:
        logger.info("Received an update without a specific user (e.g., from a channel).")
        
    await send_website_link(update, context)

# ==============================================================================
# 4. मुख्य फंक्शन (सब कुछ शुरू करने के लिए)
# ==============================================================================
def main() -> None:
    """वेबसाइट और बॉट दोनों को शुरू करता है।"""
    
    # --- वेबसाइट को एक अलग थ्रेड में शुरू करें ---
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.daemon = True
    flask_thread.start()
    
    # --- टेलीग्राम बॉट को मुख्य थ्रेड में शुरू करें ---
    application = Application.builder().token(config.BOT_TOKEN).build()

    # ---> नया: एरर हैंडलर को रजिस्टर करें <---
    application.add_error_handler(error_handler)

    application.add_handler(CommandHandler("start", send_website_link))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))

    logger.info("Starting Telegram bot polling...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
