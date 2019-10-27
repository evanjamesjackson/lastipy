from configparser import ConfigParser
import os
from src import definitions


LAST_FM_SECTION = 'LastFM'
LAST_FM_API_KEY = 'API'
SPOTIFY_SECTION = 'Spotify'
SPOTIFY_CLIENT_ID_KEY = 'CLIENT_ID'
SPOTIFY_CLIENT_SECRET_KEY = 'CLIENT_SECRET'
CONFIG_PARSER = ConfigParser()

def get_lastfm_key():
    return _get_property(LAST_FM_SECTION, LAST_FM_API_KEY)

def get_spotify_client_id():
    return _get_property(SPOTIFY_SECTION, SPOTIFY_CLIENT_ID_KEY)

def get_spotify_client_secret():
    return _get_property(SPOTIFY_SECTION, SPOTIFY_CLIENT_SECRET_KEY)

def _get_property(section, key):
    file = os.path.join(definitions.ROOT_DIR, '.keys')
    if not os.path.exists(file):
        raise Exception(".keys file is missing")

    CONFIG_PARSER.read(file)
    return CONFIG_PARSER[section][key]
