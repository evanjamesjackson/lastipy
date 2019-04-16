from configparser import ConfigParser
import os
import definitions


class ApiKeysParser:
    FILE = 'api_keys.ini'
    LAST_FM_SECTION = 'LastFM'
    API_KEY = 'API'

    def __init__(self):
        self.config_parser = ConfigParser()

    def get_lastfm_key(self):
        self.config_parser.read(self.config_parser.read(os.path.join(definitions.ROOT_DIR, self.FILE)))
        return self.config_parser[self.LAST_FM_SECTION][self.API_KEY]