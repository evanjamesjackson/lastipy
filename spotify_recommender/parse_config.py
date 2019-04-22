from configparser import ConfigParser


class ApiKeysParser:
    FILE = '.config'
    LAST_FM_SECTION = 'LastFM'
    LAST_FM_API_KEY = 'API'
    SPOTIFY_SECTION = 'Spotify'
    SPOTIFY_CLIENT_ID_KEY = 'CLIENT_ID'
    SPOTIFY_CLIENT_SECRET_KEY = 'CLIENT_SECRET'

    def __init__(self):
        self.config_parser = ConfigParser()

    def get_lastfm_key(self):
        return self._get_property(self.LAST_FM_SECTION, self.LAST_FM_API_KEY)

    def get_spotify_client_id(self):
        return self._get_property(self.SPOTIFY_SECTION, self.SPOTIFY_CLIENT_ID_KEY)

    def get_spotify_client_secret(self):
        return self._get_property(self.SPOTIFY_SECTION, self.SPOTIFY_CLIENT_SECRET_KEY)

    def _get_property(self, section, key):
        self.config_parser.read(self.FILE)
        return self.config_parser[section][key]