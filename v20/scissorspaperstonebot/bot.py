import logging
import os
import random

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")

game_keyboard = [
    ["Scissors"],
    ["Paper"],
    ["Stone"],
]
game_markup = ReplyKeyboardMarkup(game_keyboard, one_time_keyboard=True)

option_keyboard = [["Yes"], ["No"]]
option_markup = ReplyKeyboardMarkup(option_keyboard, one_time_keyboard=True)


async def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with inline buttons attached to play the game."""
    chat_id = update.message.chat.id

    msg = (
        "Hello! Thanks for using me! "
        "Let's play a game of Scissors, Paper, Stone!"
    )

    await update.message.reply_text(msg)

    await context.bot.send_message(
        chat_id=chat_id, text="Please choose:", reply_markup=game_markup
    )

    return 1


async def game_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    options = ["Scissors", "Paper", "Stone"]
    computer_choice = options[random.randint(0, 2)]

    win_msg = "I win! Better luck next time!"
    lost_msg = "Grrr... You won. I will get you next time!"
    draw_msg = "It's a tie!"

    if update.message.text == "Scissors":
        await context.bot.send_message(
            chat_id=chat_id, text=f"My choice is: {computer_choice}"
        )
        if computer_choice == "Stone":
            await update.message.reply_text(win_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
        elif computer_choice == "Paper":
            await update.message.reply_text(lost_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
        elif computer_choice == "Scissors":
            await update.message.reply_text(draw_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
    elif update.message.text == "Paper":
        await context.bot.send_message(
            chat_id=chat_id, text=f"My choice is: {computer_choice}"
        )
        if computer_choice == "Scissors":
            await update.message.reply_text(win_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
        elif computer_choice == "Stone":
            await update.message.reply_text(lost_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
        elif computer_choice == "Paper":
            await update.message.reply_text(draw_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
    elif update.message.text == "Stone":
        await context.bot.send_message(
            chat_id=chat_id, text=f"My choice is: {computer_choice}"
        )
        if computer_choice == "Paper":
            await update.message.reply_text(win_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
        elif computer_choice == "Scissors":
            await update.message.reply_text(lost_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
        elif computer_choice == "Stone":
            await update.message.reply_text(draw_msg)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup,
            )
            return 2
    else:
        await update.message.reply_text(
            f"Sorry, I do not understand your message: {update.message.text}"
        )
        await context.bot.send_message(
            chat_id=chat_id, text="Please choose:", reply_markup=game_markup
        )


async def option_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    end_msg = (
        "Thank you for using this bot!\n\n"
        "Use the /start command again if you would like to play another game!"
        "\n\nHave a great day ahead! :)"
    )

    if update.message.text == "Yes":
        await context.bot.send_message(
            chat_id=chat_id, text="Please choose:", reply_markup=game_markup
        )
        return 1
    elif update.message.text == "No":
        await context.bot.send_message(
            chat_id=chat_id, text=end_msg, reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            f"Sorry, I do not understand your message: {update.message.text}"
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text="Do you still wish to play again?",
            reply_markup=option_markup,
        )
        return 2


async def cancel(update: Update, context: CallbackContext):
    msg = "Request Cancelled. Press /start to use the bot again!"

    await update.message.reply_text(msg)
    return ConversationHandler.END


async def end(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    end_msg = (
        "Thank you for using this bot!\n\n"
        "Use the /start command again if you would like to play another game!"
        "\n\nHave a great day ahead! :)"
    )

    await context.bot.send_message(
        chat_id=chat_id, text=end_msg, reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main():
    """Run the bot."""
    # Create the Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Creates the Conversation Handler for the bot
    # to chat with user input
    game_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            1: [
                CommandHandler("end", end),
                MessageHandler(filters.TEXT, game_message)
            ],
            2: [
                CommandHandler("end", end),
                MessageHandler(filters.TEXT, option_message),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    # Add the Conversation Handler
    application.add_handler(game_conv)

    # Run the bot until user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
