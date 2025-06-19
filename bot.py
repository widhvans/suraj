# bot.py (Updated & Fixed)
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import config

# बेहतर लॉगिंग कॉन्फ़िगरेशन
# यह httpx जैसे बाहरी लाइब्रेरीज के अत्यधिक लॉग्स को शांत कर देगा
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# httpx और telegram के अपने लॉगर्स के लेवल को WARNING पर सेट करें
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("telegram.ext").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# --- आपके कमांड हैंडलर फंक्शन यहाँ रहेंगे ---
# (start, help_command, subscribe, channel functions में कोई बदलाव नहीं)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    welcome_message = (
        f"नमस्ते {user.first_name}!\n\n"
        "हमारे एजुकेशन बॉट में आपका स्वागत है। 📚\n\n"
        "हम आपको बेहतरीन स्टडी मटेरियल और कोर्सेज प्रदान करते हैं।\n"
        "आप नीचे दिए गए कमांड्स का उपयोग कर सकते हैं:\n\n"
        "/subscribe - हमारे प्रीमियम प्लान्स देखने के लिए।\n"
        "/channel - हमारा आधिकारिक टेलीग्राम चैनल ज्वाइन करने के लिए।\n"
        "/help - मदद के लिए।"
    )
    await update.message.reply_html(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "आपकी सहायता के लिए ये कमांड्स उपलब्ध हैं:\n\n"
        "/start - बॉट को शुरू करें।\n"
        "/subscribe - हमारी वेबसाइट पर सब्सक्रिप्शन प्लान्स देखें।\n"
        "/channel - हमारा टेलीग्राम चैनल ज्वाइन करें।"
    )
    await update.message.reply_text(help_text)

async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Inline keyboard buttons का कोड यहाँ रहेगा
    pass # मैंने इसे संक्षिप्तता के लिए हटा दिया है, आपका मूल कोड यहाँ सही था

async def channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Inline keyboard buttons का कोड यहाँ रहेगा
    pass # मैंने इसे संक्षिप्तता के लिए हटा दिया है, आपका मूल कोड यहाँ सही था


def main() -> None:
    """Start the bot."""
    logger.info("बॉट टोकन को कॉन्फ़िगर किया जा रहा है...")
    application = Application.builder().token(config.BOT_TOKEN).build()

    # कमांड्स को हैंडलर्स से जोड़ें
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    # आपके अन्य कमांड हैंडलर यहाँ जोड़ें
    # application.add_handler(CommandHandler("subscribe", subscribe))
    # application.add_handler(CommandHandler("channel", channel))

    # बॉट को चलाना शुरू करें
    # drop_pending_updates=True जोड़ना महत्वपूर्ण है
    logger.info("बॉट पोलिंग शुरू कर रहा है...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
