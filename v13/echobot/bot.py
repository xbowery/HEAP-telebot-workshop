import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued"""

    msg = (
        "Hello! Thanks for using my bot! This bot echoes whatever"
        " messages that you send to it. Hope you have a good day ahead!"
    )
    update.message.reply_text(msg)


def echo(update: Update, context: CallbackContext) -> None:
    """Echoes the user message"""
    message = update.message.text
    update.message.reply_text(message)


def error(update: Update, context: CallbackContext) -> None:
    """Log errors caused by updates"""
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def main():
    # Create the Updater -> Need to pass in bot's token here to init bot
    updater = Updater(TOKEN)

    # Init dispatcher to register the different handlers
    dispatcher = updater.dispatcher

    # Handle different message commands
    dispatcher.add_handler(CommandHandler("start", start))

    # Handle non-command messgaes
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # Add error handling
    dispatcher.add_error_handler(error)

    # Start running the bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed
    updater.idle()


if __name__ == "__main__":
    main()
