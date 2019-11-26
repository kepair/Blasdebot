import re
from os.path import join as os_join, dirname, abspath

PELICULA = r'PELICULA_'

IMDB = PELICULA + 'IMDB'
IMDB_LINK = 'https://www.imdb.com/title/{}'
YT_LINK = 'https://www.youtube.com/watch?v={}'
MGNT_LINK = 'http://mgnet.me/api/create'
YOUTUBE = PELICULA + 'YOUTUBE'
TORRENT = PELICULA + 'TORRENT'
SUBTITLES = PELICULA + 'SUBTITLES'
SINOPSIS = PELICULA + 'SINOPSIS'

PELICULA_REGEX = re.compile(PELICULA)

NO_TRAILER_MESSAGE = '💤 No trailer for this movie, sorry.'

LOADING_GIF = 'CgADBAADrqAAAqEeZAfb4Ot0k2Z7bAI'
cool = 'CgADBAAD46AAAuIaZAeIFKhwDWqvUQI'
acumulapunto = 'CgADBAAD46AAAuIaZAdTT7zJlgxNDQI'
green_loading = 'CgADBAAD-aAAAnUaZAfjftup41BQdAI'

LOADING_GIFS = [LOADING_GIF, cool, acumulapunto, green_loading]
