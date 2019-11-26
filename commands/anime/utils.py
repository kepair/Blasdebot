import os
import re
from collections import namedtuple
from NyaaPy import Nyaa


import requests
import logging

from commands.anime.constants import NYAA_URL

logger = logging.getLogger(__name__)

Anime = namedtuple(
    'Anime', ['name', 'magnet', 'size', 'seeders']
)


def request_anime(anime_query):
    try:
        r = requests.get(NYAA_URL)
        logger.info(r.status_code)
    except requests.exceptions.ConnectionError:
        logger.error("Nyaa is not responding.")
        return None
    if r.status_code==200:
        torrents = Nyaa.search(keyword=anime_query, category=1, subcategory=2)
        logger.info(torrents[0])
        try:
            res = torrents[0:10]
            return res
        except (IndexError, KeyError):
            logger.exception("There was a problem with Nyaa response")
            return None

def namer(name):
    #logger.info('Original: '+name)
    res = re.sub(r"^ ", "", re.sub(r"\(.*?\)", "", re.sub(r"\[.*?\]", "", name)))
    if re.search("1080",name):
        res = res + " (1080p)"
    elif re.search("720",name):
        res = res + " (720p)"
    #logger.info('Clean: '+ res)
    return res