import spotipy.util as util
from src.parse_api_keys import ApiKeysParser

REDIRECT_URI = 'https://example.com/callback/'


def get_token(username):
    keys_parser = ApiKeysParser()
    return util.prompt_for_user_token(username=username,
                                      scope='playlist-modify-public',
                                      client_id=keys_parser.get_spotify_client_id(),
                                      client_secret=keys_parser.get_spotify_client_secret(),
                                      redirect_uri=REDIRECT_URI)
