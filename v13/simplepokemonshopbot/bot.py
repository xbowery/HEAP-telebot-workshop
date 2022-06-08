import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telegram import (LabeledPrice, ReplyKeyboardMarkup, ReplyKeyboardRemove,
                      ShippingOption, Update)
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, PreCheckoutQueryHandler,
                          ShippingQueryHandler, Updater)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")
PAYMENT_PROVIDER_TOKEN = os.getenv("payment_token")

shop_keyboard = [
    ['Bulbasaur'],
    ['Charmander'],
    ['Squirtle']
]

shop_markup = ReplyKeyboardMarkup(shop_keyboard, one_time_keyboard=True)


def start(update: Update, context: CallbackContext) -> None:
    """Prints the welcome screen when the /start command is issued"""
    msg = (
        "Welcome to the Pokemon Store (Telegram version)!\n\n"
        "Please take a look at our Pokemons available by pressing the"
        " /shop command."
    )

    update.message.reply_text(msg)


def shop(update: Update, context: CallbackContext) -> None:
    """Displays the items available in the shop"""
    chat_id = update.message.chat.id

    msg = (
        "Which Pokemon would you like to purchase?"
    )

    context.bot.send_message(
        chat_id=chat_id,
        text=msg,
        reply_markup=shop_markup
    )

    return 1


def message_choice(update: Update, context: CallbackContext) -> None:
    """Detects the message to determine the user's choice"""
    chat_id = update.message.chat.id

    text = update.message.text

    if text == "Bulbasaur" or text == "Charmander" or text == "Squirtle":
        title = f"Payment for {text}"
        description = "Purchase your very own Pokemon - {text}!"
        # Select a payload just for you to recognize its the
        # donation from your bot
        payload = "Custom-Payload"
        currency = "USD"
        # Price in dollars
        price = 10
        # price * 100 so as to include 2 decimal points
        prices = [LabeledPrice("Test", price * 100)]

        context.bot.send_invoice(
            chat_id,
            title,
            description,
            payload,
            PAYMENT_PROVIDER_TOKEN,
            currency,
            prices,
            need_name=True,
            need_phone_number=True,
            need_email=True,
            need_shipping_address=True,
            is_flexible=True,
        )

        return 2

    else:
        context.bot.send_message(
            chat_id,
            text="Sorry, I don't understand your message: {text}"
        )

        msg = (
            "Which Pokemon would you like to purchase?"
        )

        context.bot.send_message(
            chat_id=chat_id,
            text=msg,
            reply_markup=shop_markup
        )

        return 1


def shipping_callback(update: Update, context: CallbackContext) -> None:
    """Answers ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # Check payload to see if matches and sent from bot
    if query.invoice_payload != "Custom-Payload":
        # Answer False ShippingQuery
        query.answer(ok=False, error_message="Something went wrong...")
        return ConversationHandler.END

    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Normal Delivery - 5 Days',
                              [LabeledPrice('Normal Charges', 300)])]
    # Second option has an array of LabeledPrice objects
    price_list = [LabeledPrice('Normal Charges', 300),
                  LabeledPrice('Express Charges', 450)]
    options.append(ShippingOption('Express Delivery - 1 Day'), price_list)
    query.answer(ok=True, shipping_options=options)


# After shipping -> PreCheckout
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Answers PreCheckoutQuery"""
    query = update.pre_checkout_query
    # Check payload to see if matches and sent from bot
    if query.invoice_payload != "Custom-Payload":
        # Answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
        return ConversationHandler.END
    else:
        query.answer(ok=True)


def successful_payment_callback(
    update: Update, context: CallbackContext
) -> None:
    """Confirms the successful payment"""
    # Do something after successfully receiving payment
    msg = (
        "Thank you for your payment!\n\n"
        "You should receive your Pokemon on "
        f"{datetime.now() + timedelta(days=1)}!"
    )

    update.message.reply_text(msg)


def cancel(update: Update, context: CallbackContext):
    msg = "Request Cancelled. Press /shop to buy another Pokemon again!"

    update.message.reply_text(msg)
    return ConversationHandler.END


def end(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    end_msg = (
        "Thank you for using this bot!\n\n"
        "Use the /shop command again if you would like to purchase a Pokemon!"
        "\n\nHave a great day ahead! :)"
    )

    context.bot.send_message(
        chat_id=chat_id, text=end_msg, reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def error(update: Update, context: CallbackContext) -> None:
    """Log errors caused by updates"""
    logger.warning("Update '%s' caused error '%s'", update, context.error)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it the bot's token
    updater = Updater(TOKEN)

    # Init dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add start handler
    dispatcher.add_handler(CommandHandler("start", start))

    # Creates the Conversation Handler for the bot
    # to chat with user input
    shop_conv = ConversationHandler(
        entry_points=[CommandHandler("shop", shop)],
        states={
            1: [
                CommandHandler("end", end),
                MessageHandler(Filters.text, message_choice)
            ],
            2: [
                CommandHandler("end", end),
                ShippingQueryHandler(shipping_callback),
                PreCheckoutQueryHandler(precheckout_callback),
                MessageHandler(Filters.successful_payment,
                               successful_payment_callback)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    # Add conversation handler
    dispatcher.add_handler(shop_conv)

    # Add error handler
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed
    updater.idle()


if __name__ == "__main__":
    main()
