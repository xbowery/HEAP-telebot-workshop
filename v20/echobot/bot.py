import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, filters)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued"""

    msg = (
        "Hello! Thanks for using my bot! This bot echoes whatever"
        " messages that you send to it. Hope you have a good day ahead!"
    )
    await update.message.reply_text(msg)


async def echo(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Echoes the user message"""
    message = update.message.text
    await update.message.reply_text(message)


async def error(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Log errors caused by updates"""
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def main():
    """Run the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add Command handlers
    application.add_handler(CommandHandler("start", start))

    # Add Message handlers
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    )

    # Run the bot until user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
