import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ChatMemberStatus
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = "7755314548:AAEbn3EhrlLWxxw5swAJhDfo8FQzeBN9lr8"
CHANNEL_USERNAME = "@YOUR_CHANNEL_USERNAME"  # Replace with your actual channel username

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"\U0001F44B Hi {user.first_name}!\n"
        "Before you can use this bot, please join our channel:\n"
        f"{CHANNEL_USERNAME}\n"
        "Once you've joined, click the button below to continue.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")]]
        ),
        parse_mode="Markdown"
    )

async def check_membership(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    try:
        chat_member = await context.bot.get_chat_member(CHANNEL_USERNAME, user.id)

        if chat_member.status in [ChatMemberStatus.MEMBER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await update.message.reply_text("\u2705 You are a member of the channel. You can now use the bot.")
        else:
            await start(update, context)  # Prompt the user to join the channel again
    except Exception as e:
        await update.message.reply_text(f"\u26A0\uFE0F An error occurred: {e}")

async def invalid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "\u26A0\uFE0F\u274C Invalid command. Please use /start to restart the bot.",
        parse_mode="Markdown"
    )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.COMMAND, invalid_command))

    print("\U0001F916 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
