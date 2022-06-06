import os
import logging
import random
import telegram
from dotenv import load_dotenv

from telegram import (
    ReplyKeyboardMarkup,
    Update,
    ReplyKeyboardRemove,
)

from telegram.ext import (
    Updater,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    CallbackQueryHandler,
    CallbackContext,
    Filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")

game_keyboard = [
    ['Scissors'],
    ['Paper'],
    ['Stone'],
]
game_markup = ReplyKeyboardMarkup(game_keyboard, one_time_keyboard=True)

option_keyboard = [['Yes'], ['No']]
option_markup = ReplyKeyboardMarkup(option_keyboard, one_time_keyboard=True)

def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with the three inline buttons attached to play the game."""
    chat_id = update.message.chat.id

    update.message.reply_text("Hello! Thanks for using me! Let's play a game of Scissors, Paper, Stone!")

    context.bot.send_message(
        chat_id=chat_id,
        text="Please choose:",
        reply_markup=game_markup
    )

    return 1

def game_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    options = ['Scissors', 'Paper', 'Stone']
    computer_choice = options[random.randint(0, 2)]

    if update.message.text == 'Scissors':
        context.bot.send_message(
            chat_id=chat_id,
            text="My choice is: {}".format(computer_choice)
        )
        if computer_choice == 'Stone':
            update.message.reply_text('I win! Better luck next time!')
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
        elif computer_choice == 'Paper':
            update.message.reply_text("Grrr... You won. I will get you next time!")
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
        elif computer_choice == 'Scissors':
            update.message.reply_text("It's a tie!")
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
    elif update.message.text == 'Paper':
        context.bot.send_message(
            chat_id=chat_id,
            text="My choice is: {}".format(computer_choice)
        )
        if computer_choice == 'Scissors':
            update.message.reply_text('I win! Better luck next time!')
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
        elif computer_choice == 'Stone':
            update.message.reply_text("Grrr... You won. I will get you next time!")
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
        elif computer_choice == 'Paper':
            update.message.reply_text("It's a tie!")
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
    elif update.message.text == 'Stone':
        context.bot.send_message(
            chat_id=chat_id,
            text="My choice is: {}".format(computer_choice)
        )
        if computer_choice == 'Paper':
            update.message.reply_text('I win! Better luck next time!')
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
        elif computer_choice == 'Scissors':
            update.message.reply_text("Grrr... You won. I will get you next time!")
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
        elif computer_choice == 'Stone':
            update.message.reply_text("It's a tie!")
            context.bot.send_message(
                chat_id=chat_id,
                text="Do you still wish to play again?",
                reply_markup=option_markup
            )
            return 2
    else:
        update.message.reply_text(f"Sorry, I do not understand your message: {update.message.text}")
        context.bot.send_message(
            chat_id=chat_id,
            text="Please choose:",
            reply_markup=game_markup
        )

def option_message(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    if update.message.text == 'Yes':
        context.bot.send_message(
            chat_id=chat_id,
            text="Please choose:",
            reply_markup=game_markup
        )
        return 1
    elif update.message.text == 'No':
        context.bot.send_message(
            chat_id=chat_id,
            text="Thank you for using this bot!\n\nUse the /start command again if you would like to play another game!\n\nHave a great day ahead! :)",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(f"Sorry, I do not understand your message: {update.message.text}")
        context.bot.send_message(
            chat_id=chat_id,
            text="Do you still wish to play again?",
            reply_markup=option_markup
        )
        return 2

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Request Cancelled. Press /start to use the bot again!")
    return ConversationHandler.END

def end(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    context.bot.send_message(
        chat_id=chat_id,
        text="Thank you for using this bot!\n\nUse the /start command again if you would like to play another game!\n\nHave a great day ahead! :)",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    """Runs the bot"""
    updater = Updater(TOKEN)

    dispatcher = updater.dispatcher

    game_conv = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            1: [
                CommandHandler('end', end),
                MessageHandler(Filters.text, game_message)
            ],
            2: [
                CommandHandler('end', end),
                MessageHandler(Filters.text, option_message)
            ]
        },
        fallbacks = [CommandHandler('cancel', cancel)],
        allow_reentry = True
    )

    dispatcher.add_handler(game_conv)

    updater.start_polling()

    updater.idle()

if __name__ == "__main__":
    main()