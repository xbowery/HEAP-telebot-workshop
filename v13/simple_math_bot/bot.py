import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when command /start is issued"""
    update.message.reply_text("Thanks for using my bot!")


def add(update: Update, context: CallbackContext) -> None:
    """Sum all numbers input together"""
    temp = update.message.text.split(" ")

    if len(temp) < 3:
        update.message.reply_text("Insufficient numbers provided.")
        return

    args = temp[1:]

    numbers = []

    # Checking for invalid args:
    for i in args:
        if not i.isnumeric():
            update.message.reply_text(
                "One of the numbers provided is invalid."
            )
            return

        numbers.append(int(i))

    update.message.reply_text(
        f"The sum of all the numbers provided is {sum(numbers)}"
    )


def minus(update: Update, context: CallbackContext) -> None:
    """Subtract all numbers away from the first number provded"""
    temp = update.message.text.split(" ")

    if len(temp) < 3:
        update.message.reply_text("Insufficient numbers provided.")
        return

    args = temp[1:]

    numbers = []

    # Checking for invalid args:
    for i in args:
        if not i.isnumeric():
            update.message.reply_text(
                "One of the numbers provided is invalid."
            )
            return

        numbers.append(int(i))

    big_number = numbers[0]
    numbers = numbers[1:]

    reply_msg = (
        "The result of the difference of all the numbers provided is "
        f"{big_number - sum(numbers)}"
    )

    update.message.reply_text(reply_msg)


def multiply(update: Update, context: CallbackContext) -> None:
    temp = update.message.text.split(" ")

    if len(temp) < 3:
        update.message.reply_text("Insufficient numbers provided.")
        return

    args = temp[1:]

    numbers = []

    # Checking for invalid args:
    for i in args:
        if not i.isnumeric():
            update.message.reply_text(
                "One of the numbers provided is invalid."
            )
            return

        numbers.append(int(i))

    result = 1
    for i in numbers:
        result *= i

    update.message.reply_text(
        f"The product of all the numbers provided is {result}"
    )


def divide(update: Update, context: CallbackContext) -> None:
    temp = update.message.text.split(" ")

    if len(temp) != 3:
        update.message.reply_text("Please only provide 2 numbers.")
        return

    args = temp[1:]

    numbers = []

    # Checking for invalid args:
    for i in args:
        if not i.isnumeric():
            update.message.reply_text(
                "One of the numbers provided is invalid."
            )
            return

        numbers.append(int(i))

    result = numbers[0] / numbers[1]

    update.message.reply_text(
        f"The quotient of the numbers provided is {result}"
    )


def error(update: Update, context: CallbackContext) -> None:
    """Log errors caused by updates"""
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def main():
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("minus", minus))
    dispatcher.add_handler(CommandHandler("multiply", multiply))
    dispatcher.add_handler(CommandHandler("divide", divide))

    updater.start_polling()

    updater.idle()


if __name__ == "__main__":
    main()
