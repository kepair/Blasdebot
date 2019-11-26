import telegram
from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async

import datetime

# SYSTEM library
import os

from utils.decorators import send_typing_action
from utils.config import USER_IDS


reply_keyboard = [['/movie'],['/anime']]

markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard = True)


@send_typing_action
def start(bot, update):
    bot.send_message(chat_id = update.message.chat_id, text = "Hi!\nI try to make torrent search easier. I'll improve, promise.", reply_markup = markup)
    print(datetime.datetime.now())
    print("User {} started the bot!".format(update.message.chat_id))


start_handler = CommandHandler('start', start, Filters.user(user_id=USER_IDS))