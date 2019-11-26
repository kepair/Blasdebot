# Python-telegram-bot libraries
import telegram 
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async

# Logging and requests libraries
import logging

from utils.decorators import send_typing_action
from utils.config import USER_IDS
from commands.anime.utils import request_anime, namer
from commands.pelicula.callback import make_tiny

logger = logging.getLogger(__name__)


# '/updateIP' command
@send_typing_action
def anime_message(bot, update, chat_data, **kwargs):
    anime = kwargs.get('args')
    if not anime:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='You need to give me a name like this: `/anime <name>`',
            parse_mode='markdown',
        )
        return
    anime_query = ' '.join(anime)
    anime_res = request_anime(anime_query)

    if anime_res!=None:
        list = []
        for x in anime_res:
            url = make_tiny(x['magnet'])
            list.append('-'*20)
            list.append(
                namer(x['name'])+
                '\n 🗳 Size: '+x['size']+' 🌱 Seeds: '+x['seeders']+'\n'+'[More info]('+x['url']+') - [Magnet]('+url+')')
            #Use regex to remove brakets
        bot.send_message(
            chat_id = update.message.chat_id, 
            text = '\n'.join(list), 
            parse_mode='markdown')
        return
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='Nyaa is down or there\'s no result for `%s`' % anime_query,
            parse_mode='markdown')
        return
        

anime_message_handler = CommandHandler('anime', anime_message, Filters.user(user_id=USER_IDS), pass_args=True, pass_chat_data=True)