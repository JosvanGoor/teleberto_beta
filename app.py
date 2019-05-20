import logging
import traceback
from dieroller.parser import Parser
from token import get_token

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext import Filters
import json

dieroller = Parser()

logfilename = "logfile.txt"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def message(bot, update):
    print("received message from {}: {}".format(update.message.chat_id, update.message.text))

    text = update.message.text

    if text.startswith("/roll ") and len(text) > 6:
        command = text[6:]
        try:
            ast = dieroller.parse(command)
            bot.send_message(update.message.chat_id, "Je rolde {}".format(ast.evaluate()))
        except Exception as e:
            traceback.print_exc()
            bot.send_message(update.message.chat_id, "Foutje!: {}".format(e))

    if text.startswith("/rollv ") and len(text) > 7:
        command = text[7:]
        try:
            ast = dieroller.parse(command)
            str, val = ast.stringify()

            if len(str) > 4000:
                bot.send_message(update.message.chat_id, "Message too long, omitted...\nJe rolde: {}".format(val))
            else:
                bot.send_message(update.message.chat_id, "Je rolde {}\n = {}".format(str, val))
        except Exception as e:
            bot.send_message(update.message.chat_id, "Foutje!: {}".format(e))

updater = Updater(get_token())
updater.dispatcher.add_handler(MessageHandler((Filters.text | Filters.command), message))

updater.start_polling()
updater.idle()
