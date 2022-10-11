from collections import defaultdict
import logging
from telegram import Update
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from src.utils import DuplicateError, find

from .datastore import DataStore


logger = logging.getLogger(__name__)


COMPANY_NAME, COMPANY_WEBSITE, COMPANY_DESCRIPTION = range(3)


class Company:
    datastore = DataStore("company", cols=["name", "website", "description"])
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
                f"Company already exists with name '{self.data[id]['name']}'"
            )

        data = self.data.pop(id)
        self.datastore.insert(list(data.values()))
        logger.info("Added company", data)
        return self.get(data)


company = Company()


async def addcompany(update: Update, context):
    logger.info("addcompany: %s" % update.message.text)
    await update.message.reply_text(
        "Now I will ask you some basic info about company. "
        "Send /cancel to stop answering to me.\n\n"
        "What is company name?"
    )
    return COMPANY_NAME


async def addcompany_name(update: Update, context):
    logger.info("addcompany_name: %s" % update.message.text)
    company.add_name(update.effective_user.id, update.message.text)
    await update.message.reply_text(
        "Looks good! Now, send company's website, or send /skip it you don't want to."
    )
    return COMPANY_WEBSITE


async def addcompany_website(update: Update, context):
    logger.info("addcompany_website: %s" % update.message.text)
    company.add_website(update.effective_user.id, update.message.text)
    await update.message.reply_text(
        "Gorgeous! Now, Tell me some brief description about the company,"
        "or send /skip if you don't want to"
    )
    return COMPANY_DESCRIPTION


async def skip_addcompany_website(update: Update, context):
    logger.info("skip_addcompany_website: %s" % update.message.text)
    await update.message.reply_text(
        "No problem! Now, Tell me some brief description about the company,"
        "or send /skip if you don't want to"
    )
    return COMPANY_DESCRIPTION


async def addcompany_description(update: Update, context):
    logger.info("addcompany_description: %s" % update.message.text)

    company.add_des(update.effective_user.id, update.message.text)

    try:
        res = company.commit(update.effective_user.id)
        await update.message.reply_text(
            f"Done! We have add a company with following details\n{res}"
        )
        return ConversationHandler.END

    except DuplicateError as e:
        logger.error(e)
        await update.message.reply_text(f"Error: {e}")
        return ConversationHandler.END


async def skip_addcompany_description(update: Update, context):
    logger.info("skip_addcompany_description: %s" % update.message.text)

    try:
        res = company.commit(update.effective_user.id)
        await update.message.reply_text(
            "Done! We have add a company with following details\n" f"{res}"
        )
        return ConversationHandler.END

    except DuplicateError as e:
        logger.error(e)
        await update.message.reply_text(f"Error: {e}")
        return ConversationHandler.END


async def cancel_addcompany(update: Update, context):
    logger.info("cancel addcompany")

    company.cancel(update.effective_user.id)
    await update.message.reply_text("No problem! Type /help for other commands.")

    return ConversationHandler.END


company_conversion_handler = ConversationHandler(
    entry_points=[CommandHandler("addcompany", addcompany)],
    states={
        COMPANY_NAME: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, addcompany_name)
        ],
        COMPANY_WEBSITE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, addcompany_website),
            CommandHandler("skip", skip_addcompany_website),
        ],
        COMPANY_DESCRIPTION: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, addcompany_description),
            CommandHandler("skip", skip_addcompany_description),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel_addcompany)],
)
