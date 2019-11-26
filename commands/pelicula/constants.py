import re

PELICULA = r'PELICULA_'

IMDB = PELICULA + 'IMDB'
IMDB_LINK = 'https://www.imdb.com/title/{}'
YT_LINK = 'https://www.youtube.com/watch?v={}'
MGNT_LINK = 'http://mgnet.me/api/create'
YOUTUBE = PELICULA + 'YOUTUBE'
TORRENT = PELICULA + 'TORRENT'
SINOPSIS = PELICULA + 'SINOPSIS'

PELICULA_REGEX = re.compile(PELICULA)

NO_TRAILER_MESSAGE = '💤 No trailer for this movie, sorry.'
