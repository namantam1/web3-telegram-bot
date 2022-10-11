import logging
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from .datastore import DataStore
from collections import defaultdict
from .utils import find, DuplicateError


logger = logging.getLogger(__name__)


INVESTOR_NAME, INVESTOR_WEBSITE, INVESTOR_DESCRIPTION = range(3)


class Investor:
    datastore = DataStore("investor", cols=["name", "website", "description"])
    data = defaultdict(lambda: {"name": "", "website": "", "description": ""})

    def add_name(self, id, name):
        self.data[id]["name"] = name

    def add_website(self, id, website):
        self.data[id]["website"] = website

    def add_des(self, id, des):
        self.data[id]["description"] = des

    def get(self, data):
        return (
            f"Name - {data['name']}\n"
            f"Website - {data['website']}\n"
            f"Description - {data['description']}"
        )

    def cancel(self, id):
        self.data.pop(id, None)

    def commit(self, id):
        if (
            find(self.datastore.data, lambda val: val[0] == self.data[id]["name"])
            is not None
        ):
            raise DuplicateError(
                f"Investor already exists with name '{self.data[id]['name']}'"
            )

        data = self.data.pop(id)
        self.datastore.insert(list(data.values()))
        logger.info("Added investor", data)
        return self.get(data)


investor = Investor()


async def add(update: Update, context):
    logger.info("addinvestor: %s" % update.message.text)
    await update.message.reply_text(
        "Now I will ask you some basic info about investor. "
        "Send /cancel to stop answering to me.\n\n"
        "What is investor name?"
    )
    return INVESTOR_NAME


async def add_name(update: Update, context):
    logger.info("addinvestor_name: %s" % update.message.text)
    investor.add_name(update.effective_user.id, update.message.text)
    await update.message.reply_text(
        "Looks good! Now, send investor's website, or send /skip it you don't want to."
    )
    return INVESTOR_WEBSITE


async def add_website(update: Update, context):
    logger.info("addinvestor_website: %s" % update.message.text)
    investor.add_website(update.effective_user.id, update.message.text)
    await update.message.reply_text(
        "Gorgeous! Now, Tell me some brief description about the investor,"
        "or send /skip if you don't want to"
    )
    return INVESTOR_DESCRIPTION


async def skip_add_website(update: Update, context):
    logger.info("skip_addinvestor_website: %s" % update.message.text)
    await update.message.reply_text(
        "No problem! Now, Tell me some brief description about the investor,"
        "or send /skip if you don't want to"
    )
    return INVESTOR_DESCRIPTION


async def add_description(update: Update, context):
    logger.info("addinvestor_description: %s" % update.message.text)

    investor.add_des(update.effective_user.id, update.message.text)

    try:
        res = investor.commit(update.effective_user.id)
        await update.message.reply_text(
            f"Done! We have add a investor with following details\n{res}"
        )
        return ConversationHandler.END

    except DuplicateError as e:
        logger.error(e)
        await update.message.reply_text(f"Error: {e}")
        return ConversationHandler.END


async def skip_add_description(update: Update, context):
    logger.info("skip_addinvestor_description: %s" % update.message.text)

    try:
        res = investor.commit(update.effective_user.id)
        await update.message.reply_text(
            "Done! We have add a investor with following details\n" f"{res}"
        )
        return ConversationHandler.END

    except DuplicateError as e:
        logger.error(e)
        await update.message.reply_text(f"Error: {e}")
        return ConversationHandler.END


async def cancel_add(update: Update, context):
    logger.info("cancel addinvestor")

    investor.cancel(update.effective_user.id)
    await update.message.reply_text("No problem! Type /help for other commands.")

    return ConversationHandler.END


investor_conversion_handler = ConversationHandler(
    entry_points=[CommandHandler("addinvestor", add)],
    states={
        INVESTOR_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_name)],
        INVESTOR_WEBSITE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_website),
            CommandHandler("skip", skip_add_website),
        ],
        INVESTOR_DESCRIPTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, add_description),
            CommandHandler("skip", skip_add_description),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_add)],
)
