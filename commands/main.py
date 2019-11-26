# -*- coding: utf-8 -*-
# Python-telegram-bot libraries
import telegram
from telegram import ReplyKeyboardMarkup, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async

# Logging and requests libraries
import logging
import requests

# Import token from config file
from commands.pelicula.callback import peliculas_callback
from commands.pelicula.command import movie_handler
from commands.start.command import start_handler
from commands.unknown.command import unknown_handler
from commands.anime.command import anime_message_handler
from utils.decorators import send_typing_action
from utils.config import token

updater = Updater(token = token)
dispatcher = updater.dispatcher
bot = telegram.Bot(token = token)

# Logging module for debugging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Reply Keyboard
reply_keyboard = [['/movie'],['/anime']]
markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard = True)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(movie_handler)
dispatcher.add_handler(peliculas_callback)
dispatcher.add_handler(anime_message_handler)
dispatcher.add_handler(unknown_handler)


# Module to start getting data
updater.start_polling()
updater.idle()
