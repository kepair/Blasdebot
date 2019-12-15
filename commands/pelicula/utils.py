import os
from collections import namedtuple

import requests
import logging

from utils.config import MYTVDB_API_KEY

from babelfish import Language
from subliminal import download_best_subtitles, save_subtitles, Movie
from subliminal.subtitle import get_subtitle_path

from commands.pelicula.constants import YT_LINK

logger = logging.getLogger(__name__)

Pelicula = namedtuple(
    'Pelicula', ['title', 'original_title', 'rating', 'overview', 'year', 'image']
)


def request_movie(pelicula_query):
    params = {
        'api_key': MYTVDB_API_KEY,
        'query': pelicula_query,
        'language': 'en-US',
    }
    r = requests.get('https://api.themoviedb.org/3/search/movie', params=params)
    if r.status_code == 200:
        try:
            return r.json()['results'][0]
        except (IndexError, KeyError):
            return None


def get_basic_info(movie):
    title = movie['title']
    original_title = movie.get('original_title')
    rating = movie['vote_average']
    overview = movie['overview']
    year = movie['release_date'].split('-')[0]  # "2016-07-27" -> 2016
    image_link = movie['backdrop_path']
    poster = f"http://image.tmdb.org/t/p/original{image_link}" if image_link else None
    return Pelicula(title, original_title, rating, overview, year, poster)


def prettify_basic_movie_info(peli, with_overview=True):
    stars = rating_stars(peli.rating)
    overview = peli.overview if with_overview else ''
    title = _title_header(peli)
    return (
               f"{title}"
               f"{stars}\n\n"
               f"{overview}"
           ), peli.image

def _title_header(peli):
    if peli.original_title:
        return f"{peli.title} ({peli.original_title}) ~ {peli.year}\n"
    else:
        return f"{peli.title} ({peli.year})\n"


def get_yt_trailer(videos):
    try:
        key = videos['results'][-1]['key']
    except (KeyError, IndexError):
        return None

    return YT_LINK.format(key)


def get_yts_torrent_info(imdb_id):
    yts_api = 'https://yts.ae/api/v2/list_movies.json'
    try:
        logger.info(imdb_id)
        r = requests.get(yts_api, params={"query_term": imdb_id})
    except requests.exceptions.ConnectionError:
        return None
    if r.status_code == 200:
        torrent = r.json()  # Dar url en lugar de hash.
        try:
            torrents = torrent["data"]["movies"][0]['torrents']
            movie = get_best_torrent(torrents)
            url = movie['url']
            seeds = movie['seeds']
            size = movie['size']
            quality = movie['quality']
            #logger.exception(movie['hash'])
            #logger.exception(torrent['data']['movies'][0]['url'])
            magnet = "magnet:?xt=urn:btih:"+movie['hash']+"&dn="+torrent['data']['movies'][0]['url']+"&tr=udp://open.demonii.com:1337/announce&tr=udp://tracker.openbittorrent.com:80&tr=udp://tracker.coppersurfer.tk:6969&tr=udp://glotorrents.pw:6969/announce&tr=udp://tracker.opentrackr.org:1337/announce&tr=udp://torrent.gresille.org:80/announce"
            return url, seeds, size, quality, magnet

        except (IndexError, KeyError):
            logger.exception("There was a problem with yts api response")
            return None

def get_best_torrent(torrents):
    #Is there a 1080p torrent?
    movie = next((item for item in torrents if item['quality'] == '1080p'), None)
    #If magnet is None, then search for 720p
    if movie==None:
        movie = next((item for item in torrents if item['quality'] == '720p'), None)
    return movie


def rating_stars(rating):
    """Transforms int rating into stars with int"""
    stars = int(rating // 2)
    rating_stars = f"{'⭐'*stars} ~ {rating}"
    return rating_stars
