from configparser import ConfigParser
import os
import definitions


class ApiKeysParser:
    FILE = 'api_keys.ini'
    LAST_FM_SECTION = 'LastFM'
    API_KEY = 'API'
    SPOTIFY_SECTION = 'Spotify'
    SPOTIFY_CLIENT_ID_KEY = 'CLIENT_ID'
    SPOTIFY_CLIENT_SECRET_KEY = 'CLIENT_SECRET'

    def __init__(self):
        self.config_parser = ConfigParser()

    def get_lastfm_key(self):
        return self._get_property(self.LAST_FM_SECTION, self.API_KEY)

    def get_spotify_client_id(self):
        return self._get_property(self.SPOTIFY_SECTION, self.SPOTIFY_CLIENT_ID_KEY)

    def get_spotify_client_secret(self):
        return self._get_property(self.SPOTIFY_SECTION, self.SPOTIFY_CLIENT_SECRET_KEY)

    def _get_property(self, section, key):
        self.config_parser.read(os.path.join(definitions.ROOT_DIR, self.FILE))
        return self.config_parser[section][key]