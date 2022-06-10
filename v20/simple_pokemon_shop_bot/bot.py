import logging
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import (Application, CallbackContext, CommandHandler,
                          MessageHandler, PreCheckoutQueryHandler,
                          ShippingQueryHandler, filters)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv("../.env")
TOKEN = os.getenv("token")
PAYMENT_PROVIDER_TOKEN = os.getenv("payment_token")


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Prints the welcome screen when the /start command is issued"""
    msg = (
        "Welcome to the Pokemon Store (Telegram version)!\n\n"
        "Please purchase our Pokemon by pressing the"
        " /pokemon command."
    )

    await update.message.reply_text(msg)


async def pokemon_choice(
    update: Update, context: CallbackContext.DEFAULT_TYPE
) -> None:
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

    await context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        PAYMENT_PROVIDER_TOKEN,
        currency,
        prices,
        photo_url="https://i.imgur.com/0Zogxhb.png",
        photo_width=512,
        photo_height=512,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )


async def shipping_callback(
    update: Update, context: CallbackContext.DEFAULT_TYPE
) -> None:
    """Answers ShippingQuery with ShippingOptions"""
    query = update.shipping_query
    # Check payload to see if matches and sent from bot
    if query.invoice_payload != "Custom-Payload":
        # Answer False ShippingQuery
        await query.answer(ok=False, error_message="Something went wrong...")
        return

    # First option has a single LabeledPrice
    options = [ShippingOption('1', 'Normal Delivery - 5 Days',
                              [LabeledPrice('Normal Charges', 300)])]
    # Second option has an array of LabeledPrice objects
    price_list = [LabeledPrice('Normal Charges', 300),
                  LabeledPrice('Express Charges', 450)]
    options.append(ShippingOption('2', 'Express Delivery - 1 Day', price_list))
    await query.answer(ok=True, shipping_options=options)


# After shipping -> PreCheckout
async def precheckout_callback(
    update: Update, context: CallbackContext.DEFAULT_TYPE
) -> None:
    """Answers PreCheckoutQuery"""
    query = update.pre_checkout_query
    # Check payload to see if matches and sent from bot
    if query.invoice_payload != "Custom-Payload":
        # Answer False pre_checkout_query
        await query.answer(ok=False, error_message="Something went wrong...")
        return
    else:
        await query.answer(ok=True)


async def successful_payment_callback(
    update: Update, context: CallbackContext.DEFAULT_TYPE
) -> None:
    """Confirms the successful payment"""
    # Do something after successfully receiving payment
    date = datetime.now() + timedelta(days=1)
    date = str(date).split(" ")[0]
    msg = (
        "Thank you for your payment!\n\n"
        "You should receive your Pokemon on "
        f"{date}!"
    )

    await update.message.reply_text(msg)


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it the bot's token
    application = Application.builder().token(TOKEN).build()

    # Add start handler
    application.add_handler(CommandHandler("start", start))

    # Add handlers
    application.add_handler(CommandHandler("pokemon", pokemon_choice))
    application.add_handler(ShippingQueryHandler(shipping_callback))
    application.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT,
                                           successful_payment_callback))

    # Run the bot until user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
