# bot.py
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes
import config

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start कमांड का फंक्शन
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

# /help कमांड का फंक्शन
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_text = (
        "आपकी सहायता के लिए ये कमांड्स उपलब्ध हैं:\n\n"
        "/start - बॉट को शुरू करें।\n"
        "/subscribe - हमारी वेबसाइट पर सब्सक्रिप्शन प्लान्स देखें।\n"
        "/channel - हमारा टेलीग्राम चैनल ज्वाइन करें।"
    )
    await update.message.reply_text(help_text)

# /subscribe कमांड का फंक्शन
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("⭐ हमारे प्लान्स देखें", url=config.WEBSITE_URL)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "हमारे प्रीमियम सब्सक्रिप्शन प्लान्स देखने और खरीदने के लिए नीचे दिए गए बटन पर क्लिक करें:",
        reply_markup=reply_markup
    )

# /channel कमांड का फंक्शन
async def channel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("🚀 चैनल ज्वाइन करें", url=config.STUDY_CHANNEL_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "नवीनतम अपडेट, नोट्स और स्टडी मटेरियल के लिए हमारा आधिकारिक टेलीग्राम चैनल ज्वाइन करें:",
        reply_markup=reply_markup
    )

def main() -> None:
    """Start the bot."""
    # बॉट का Application ऑब्जेक्ट बनाएं
    application = Application.builder().token(config.BOT_TOKEN).build()

    # कमांड्स को हैंडलर्स से जोड़ें
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("subscribe", subscribe))
    application.add_handler(CommandHandler("channel", channel))

    # बॉट को चलाना शुरू करें
    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
