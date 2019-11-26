import os
import logging
import random

import requests
from telegram.ext import CallbackQueryHandler
from utils.config import MYTVDB_API_KEY



from commands.pelicula.constants import (
    IMDB,
    IMDB_LINK,
    MGNT_LINK,
    YOUTUBE,
    TORRENT,
    SINOPSIS,
    NO_TRAILER_MESSAGE,
    SUBTITLES,
    LOADING_GIFS,
    PELICULA_REGEX)
from commands.pelicula.keyboard import pelis_keyboard
from commands.pelicula.utils import (
    get_yts_torrent_info,
    get_yt_trailer,
    prettify_basic_movie_info
)

logger = logging.getLogger(__name__)


def pelicula_callback(bot, update, chat_data):
    context = chat_data.get('context')
    if not context:
        user = update.effective_user.first_name
        message = (
            f"Couldn't get the requested info. {user}, please forgive me.\n"
            f"Try again."
        )
        bot.send_message(
            chat_id=update.callback_query.message.chat_id,
            text=message,
            parse_mode='markdown',
        )
        # Notify telegram we have answered
        update.callback_query.answer(text='')
        return

    answer = update.callback_query.data
    logger.info('User choice: %s', answer)
    response = handle_answer(bot, update, context['data'], answer)
    if response:
        update.callback_query.answer(text='')
        message, image = prettify_basic_movie_info(
            context['data']['movie_basic'], with_overview=False
        )
        updated_message = '\n'.join((message, response))

        update.callback_query.message.edit_text(
            text=updated_message,
            reply_markup=pelis_keyboard(include_desc=True),
            parse_mode='markdown',
            quote=False,
        )
    else:
        logger.info(
            "Handled response: %s. Answer: %s, context: %s",
            response,
            answer,
            context['data'],
        )


def handle_answer(bot, update, data, link_choice):
    """Gives link_choice of movie id.

    link_choice in ('IMDB', 'Magnet', 'Youtube', 'Subtitles')
    """
    params = {'api_key': MYTVDB_API_KEY, 'append_to_response': 'videos'}
    r = requests.get(f"https://api.themoviedb.org/3/movie/{data['movie']['id']}", params=params)
    movie_data = r.json()
    imdb_id = movie_data['imdb_id']

    if link_choice == IMDB:
        answer = f"[IMDB]({IMDB_LINK.format(imdb_id)}"

    if link_choice == SINOPSIS:
        pelicula = data['movie_basic']
        answer = pelicula.overview

    elif link_choice == YOUTUBE:
        trailer = get_yt_trailer(movie_data['videos'])
        answer = f"[Trailer]({trailer})" if trailer else NO_TRAILER_MESSAGE

    elif link_choice == TORRENT:
        torrent = get_yts_torrent_info(imdb_id)
        if torrent:
            url, seeds, size, quality, magnet = torrent
            shorturl = make_tiny(magnet)
            answer = (
                f"📤 [{data['movie']['title']}]({url})\n\n"
                f"🌱 Seeds: {seeds}\n\n"
                f"🗳 Size: {size}\n\n"
                f"🖥 Quality: {quality}\n\n"
                f"{shorturl}\n\n"
                f"\n\n"
            )
        else:
            answer = "🚧 No torrent available for this movie."

    return answer

def make_tiny(magnet): 
    res = requests.get(MGNT_LINK, params={"m": magnet,"format": "json"}).json()
    return res['shorturl']     

peliculas_callback = CallbackQueryHandler(pelicula_callback, pattern=PELICULA_REGEX, pass_chat_data=True)
