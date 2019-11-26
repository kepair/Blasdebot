import telegram
from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async

import datetime

from utils.decorators import send_typing_action


@send_typing_action
def unknown(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text="What language is this? Please try again!")

    print(datetime.datetime.now())
    print("User {} called an unknown command!".format(update.message.chat_id))

unknown_handler = MessageHandler(Filters.command, unknown)
