import requests
from telegram.ext import run_async, CommandHandler, Filters

from commands.pelicula.keyboard import pelis_keyboard
from commands.pelicula.utils import (
    request_movie,
    get_basic_info,
    prettify_basic_movie_info,
)
from utils.decorators import send_typing_action



@send_typing_action
def buscar_peli(bot, update, chat_data, **kwargs):
    pelicula = kwargs.get('args')
    if not pelicula:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='I need a movie name `/pelicula <name>`',  # Todo: Add deeplink with example
            parse_mode='markdown',
        )
        return

    try:
        pelicula_query = ' '.join(pelicula)
        movie = request_movie(pelicula_query)
        if not movie:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Couldn\'t find info for %s' % pelicula_query,
            )
            return

        movie_info = get_basic_info(movie)
        # Give context to button handlers
        chat_data['context'] = {
            'data': {'movie': movie, 'movie_basic': movie_info},
            'command': 'pelicula',
            'edit_original_text': True,
        }

        movie_details, poster = prettify_basic_movie_info(movie_info)
        if poster:
            bot.send_photo(chat_id=update.message.chat_id, photo=poster)

        update.message.reply_text(
            text=movie_details,
            reply_markup=pelis_keyboard(),
            parse_mode='markdown',
            disable_web_page_preview=True,
            quote=False,
        )
    except requests.exceptions.ConnectionError:
        bot.send_message(
            chat_id=update.message.chat_id,
            text='There has been a connection error. ¿?',
            parse_mode='markdown',
        )
movie_handler = CommandHandler('movie', buscar_peli, pass_args=True, pass_chat_data=True)