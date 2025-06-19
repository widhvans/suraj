# bot.py (Updated for sending website link)

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import config

# लॉगिंग कॉन्फ़िगरेशन (पहले जैसा ही)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# यह फंक्शन वेबसाइट का लिंक भेजने का काम करेगा
async def send_website_link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with a button to the hosted website."""
    
    # कीबोर्ड बटन जो वेबसाइट के लिंक की ओर ले जाएगा
    keyboard = [
        [InlineKeyboardButton("🌐 हमारी वेबसाइट पर जाएं", url=config.WEBSITE_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # भेजा जाने वाला मैसेज
    message_text = (
        "नमस्ते! 👋\n\n"
        "हमारी सेवाओं और सब्सक्रिप्शन प्लान की पूरी जानकारी के लिए, कृपया हमारी वेबसाइट पर जाएं।\n\n"
        f"आप सीधे इस लिंक पर भी क्लिक कर सकते हैं: {config.WEBSITE_URL}"
    )

    # यूजर को मैसेज भेजें
    await update.message.reply_text(message_text, reply_markup=reply_markup)


# यह फंक्शन किसी भी टेक्स्ट मैसेज का जवाब देगा (कमांड को छोड़कर)
async def handle_any_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles any non-command text message by sending the website link."""
    logger.info(f"Received a non-command message from {update.effective_user.first_name}")
    await send_website_link(update, context)


def main() -> None:
    """Start the bot."""
    # एप्लीकेशन ऑब्जेक्ट बनाना
    application = Application.builder().token(config.BOT_TOKEN).build()

    # 1. /start कमांड के लिए हैंडलर
    # जब कोई बॉट को स्टार्ट करेगा, तो उसे लिंक मिलेगा
    application.add_handler(CommandHandler("start", send_website_link))

    # 2. किसी भी टेक्स्ट मैसेज के लिए हैंडलर
    # अगर यूजर /start के अलावा कुछ भी लिखता है (जैसे "hello", "link do", आदि), तो भी उसे लिंक मिलेगा
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_any_message))

    # बॉट को चलाना शुरू करें
    logger.info("Bot is starting in link-sending mode...")
    application.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
