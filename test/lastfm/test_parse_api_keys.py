from src.lastfm.parse_api_keys import ApiKeysParser
import unittest

class ApiKeysParserTest(unittest.TestCase):
    def test_get_lastfm_key(self):
        parser = ApiKeysParser()
        key = parser.get_lastfm_key()
        self.assertIsNotNone(key)