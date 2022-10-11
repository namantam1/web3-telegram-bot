from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.datastore import DataStore

import logging

logger = logging.getLogger(__name__)


info_text = (
    "Hey {name}, Welcome to web3 information bot. Using this bot you can add, remove information about"
    " companies and investor and get their data on an excel sheet"
)
command_text = (
    "Following commands are avaialbe:\n"
    "/addcompany - To add a new company\n"
    "/addinvestor - To add a new investor\n"
    "/share - To get sheet url\n"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("start called")
    await update.message.reply_text(
        f"{info_text.format(name=update.effective_user.full_name)}\n\n"
        f"{command_text}"
    )


async def help(update: Update, context):
    logger.info("help called")
    await update.message.reply_text(command_text)


async def wrong_command(update: Update, contex):
    logger.info(f"Wrong command: {update.message.text}")
    await update.message.reply_text(
        "Invalid command! Please type /help or /start for more info"
    )


SHARE_URL = range(1)


async def share_start(update: Update, context):
    await update.message.reply_text(
        "Please tell your email address\n" "Enter /skip to cancel"
    )
    return SHARE_URL


async def get_url(update: Update, context):
    email = update.message.text
    DataStore.add_user(email)
    await update.message.reply_text(
        f"Added your email '{email}'. Sheet url: {DataStore.get_url()}"
    )
    logger.info(f"Added user {email}")
    return ConversationHandler.END


async def skip_share(update: Update, context):
    await update.message.reply_text("No problem! Type /help for other commands.")
    return ConversationHandler.END


share_conversion_handler = ConversationHandler(
    entry_points=[CommandHandler("share", share_start)],
    states={
        SHARE_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_url)],
    },
    fallbacks=[CommandHandler("skip", skip_share)],
)
