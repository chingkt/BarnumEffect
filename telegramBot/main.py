from telegram.ext import *

import logging
from command import *


def add_handlers(dispatcher):

    start_handler = CommandHandler("start", start, pass_update_queue=True)
    dispatcher.add_handler(start_handler)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    inline_caps_handler = InlineQueryHandler(inline_caps)
    dispatcher.add_handler(inline_caps_handler)

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

if __name__ == '__main__':
    token = "1937949766:AAFHB3frzM1xGZ40XEKsXaJmjOnQ9PYxlMA"
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    updater.start_polling()
    add_handlers(dispatcher)