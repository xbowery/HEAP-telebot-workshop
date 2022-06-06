import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CallbackContext, CommandHandler

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Send a message when command /start is issued"""
    await update.message.reply_text("Thanks for using my bot!")


async def add(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Sum all numbers input together"""
    temp = update.message.text.split(" ")

    if len(temp) < 3:
        await update.message.reply_text("Insufficient numbers provided.")
        return

    args = temp[1:]

    numbers = []

    # Checking for invalid args:
    for i in args:
        if not i.isnumeric():
            await update.message.reply_text("One of the numbers provided is invalid.")
            return

        numbers.append(int(i))

    await update.message.reply_text(
        f"The sum of all the numbers provided is {sum(numbers)}"
    )


async def minus(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Subtract all numbers away from the first number provded"""
    temp = update.message.text.split(" ")

    if len(temp) < 3:
        await update.message.reply_text("Insufficient numbers provided.")
        return

    args = temp[1:]

    numbers = []

    # Checking for invalid args:
    for i in args:
        if not i.isnumeric():
            await update.message.reply_text("One of the numbers provided is invalid.")
            return

        numbers.append(int(i))

    big_number = numbers[0]
    numbers = numbers[1:]

    reply_msg = (
        "The result of the difference of all the numbers provided is "
        f"{big_number - sum(numbers)}"
    )

    await update.message.reply_text(reply_msg)


async def multiply(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    temp = update.message.text.split(" ")

    if len(temp) < 3:
        await update.message.reply_text("Insufficient numbers provided.")
        return

    args = temp[1:]

    numbers = []

    # Checking for invalid args:
    for i in args:
        if not i.isnumeric():
            await update.message.reply_text("One of the numbers provided is invalid.")
            return

        numbers.append(int(i))

    result = 1
    for i in numbers:
        result *= i

    await update.message.reply_text(
        f"The product of all the numbers provided is {result}"
    )


async def divide(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    temp = update.message.text.split(" ")

    if len(temp) != 3:
        await update.message.reply_text("Please only provide 2 numbers.")
        return

    args = temp[1:]

    numbers = []

    # Checking for invalid args:
    for i in args:
        if not i.isnumeric():
            await update.message.reply_text("One of the numbers provided is invalid.")
            return

        numbers.append(int(i))

    result = numbers[0] / numbers[1]

    await update.message.reply_text(f"The quotient of the numbers provided is {result}")


async def error(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Log errors caused by updates"""
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def main():
    """Run the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Add Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add))
    application.add_handler(CommandHandler("minus", minus))
    application.add_handler(CommandHandler("multiply", multiply))
    application.add_handler(CommandHandler("divide", divide))

    # Run the bot until user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
