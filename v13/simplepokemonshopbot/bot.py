import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, PreCheckoutQueryHandler,
                          ShippingQueryHandler, Updater)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")
PAYMENT_PROVIDER_TOKEN = os.getenv("payment_token")


def start(update: Update, context: CallbackContext) -> None:
    """Prints the welcome screen when the /start command is issued"""
    msg = (
        "Welcome to the Pokemon Store (Telegram version)!\n\n"
        "Please purchase our Pokemon by pressing"
        " /pokemon."
    )

    update.message.reply_text(msg)


def pokemon_choice(update: Update, context: CallbackContext) -> None:
    """Detects the message to determine the user's choice"""
    chat_id = update.message.chat.id

    title = "Payment for Pikachu"
    description = "Purchase your very own Pikachu now!"
    # Select a payload just for you to recognize its the
    # donation from your bot
    payload = "Custom-Payload"
    currency = "USD"
    # Price in dollars
    price = 10
    # price * 100 so as to include 2 decimal points
    prices = [LabeledPrice("Base Price", price * 100)]

    context.bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        payload=payload,
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency=currency,
        prices=prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )


def shipping_callback(update: Update, context: CallbackContext) -> None:
    """Answers ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # Check payload to see if matches and sent from bot
    if query.invoice_payload != "Custom-Payload":
        # Answer False ShippingQuery
        query.answer(ok=False, error_message="Something went wrong...")
        return

    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Normal Delivery - 5 Days',
                              [LabeledPrice('Normal Charges', 300)])]
    # Second option has an array of LabeledPrice objects
    price_list = [LabeledPrice('Normal Charges', 300),
                  LabeledPrice('Express Charges', 450)]
    options.append(ShippingOption('2', 'Express Delivery - 1 Day'), price_list)
    query.answer(ok=True, shipping_options=options)


# After shipping -> PreCheckout
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    """Answers PreCheckoutQuery"""
    query = update.pre_checkout_query
    # Check payload to see if matches and sent from bot
    if query.invoice_payload != "Custom-Payload":
        # Answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
        return
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

    # Add handlers
    dispatcher.add_handler(CommandHandler("pokemon", pokemon_choice))
    dispatcher.add_handler(ShippingQueryHandler(shipping_callback))
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment,
                                          successful_payment_callback))

    # Add error handler
    dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Run the bot until Ctrl-C is pressed
    updater.idle()


if __name__ == "__main__":
    main()
