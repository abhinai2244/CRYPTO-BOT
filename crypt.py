import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from cryptography.fernet import Fernet
import hashlib

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = '7459618381:AAENmeJJuso2x3-WnB3MN7Lre5mPKvIS084'  # Replace with your bot token
ADMIN_ID = 5756495153  # Replace with your admin user ID

# Accessible algorithms
algorithms = {
    'aes': 'AES Encryption/Decryption',
    'sha1': 'SHA-1 Hashing',
    'md5': 'MD5 Hashing'
}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_message = (
        "👋 Welcome to the Cryptography Bot! \n"
        "This bot allows you to encrypt or hash your text using various algorithms. \n\n"
        "Choose an option below: \n"
        "1. /encrypt - Encrypt text using AES \n"
        "2. /hash - Hash text using SHA-1 or MD5\n"
        "3. /help - Get help on how to use the bot"
    )
    await update.message.reply_text(welcome_message)

# Help command handler
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    help_message = (
        "Here's how to use the bot: \n\n"
        "1. To encrypt text, send /encrypt. The bot will ask for the text you want to encrypt.\n"
        "2. To hash text, send /hash. The bot will guide you to choose SHA-1 or MD5.\n"
        "3. Send /admin to manage algorithms (admin only)."
    )
    await update.message.reply_text(help_message)

# Admin command handler to manage algorithms
async def admin_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "Admin Menu:\n"
            "You can manage algorithms here.\n\n"
            "Current active algorithms:\n"
            f"- {algorithms['aes']}\n"
            f"- {algorithms['sha1']}\n"
            f"- {algorithms['md5']}\n"
            "You can add or remove algorithms by typing them."
        )
    else:
        await update.message.reply_text("🚫 You do not have the permission to access this command.")

# Encrypting text using AES
async def encrypt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please send the text you want to encrypt.")
    context.user_data['mode'] = 'encrypt'

# Hashing text
async def hash_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Choose a hashing algorithm:\n1. SHA-1\n2. MD5")
    context.user_data['mode'] = 'hash'

# Processing user input
async def process_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    mode = context.user_data.get('mode')

    if mode == 'encrypt':
        key = Fernet.generate_key()
        cipher = Fernet(key)
        encrypted_text = cipher.encrypt(user_input.encode())
        await update.message.reply_text(f"🔒 Encrypted Text: {encrypted_text.decode()}\n🔑 Keep this key safe: {key.decode()}")
        context.user_data['mode'] = None
    elif mode == 'hash':
        if user_input == '1':
            await update.message.reply_text("Please send the text you want to hash using SHA-1.")
            context.user_data['hash_mode'] = 'sha1'
        elif user_input == '2':
            await update.message.reply_text("Please send the text you want to hash using MD5.")
            context.user_data['hash_mode'] = 'md5'
    else:
        hash_mode = context.user_data.get('hash_mode')
        if hash_mode == 'sha1':
            hash_value = hashlib.sha1(user_input.encode()).hexdigest()
            await update.message.reply_text(f"SHA-1 Hash: {hash_value}")
        elif hash_mode == 'md5':
            hash_value = hashlib.md5(user_input.encode()).hexdigest()
            await update.message.reply_text(f"MD5 Hash: {hash_value}")
        context.user_data['mode'] = None

# Main function to setup the bot
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("admin", admin_commands))
    application.add_handler(CommandHandler("encrypt", encrypt))
    application.add_handler(CommandHandler("hash", hash_text))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_input))

    application.run_polling()

if __name__ == '__main__':
    main()
