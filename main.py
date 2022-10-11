import os
from dotenv import load_dotenv
from telegram.ext import (
    CommandHandler,
    ApplicationBuilder,
    MessageHandler,
    filters,
)

from src.company import company_conversion_handler
from src.investor import investor_conversion_handler
from src.factory import share_conversion_handler, wrong_command, start, help

import logging

load_dotenv()

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    application = ApplicationBuilder().token(os.environ.get("TELEGRAM_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(share_conversion_handler)
    application.add_handler(company_conversion_handler)
    application.add_handler(investor_conversion_handler)

    # on non command i.e message
    application.add_handler(MessageHandler(filters.COMMAND, wrong_command))

    # start the application
    application.run_polling()


if __name__ == "__main__":
    main()
