import spotipy.oauth2 as oauth2
from src.parse_keys import get_spotify_client_id, get_spotify_client_secret
import webbrowser
import os
from src import definitions

REDIRECT_URI = 'https://www.example.com/callback/'


#TODO test
def get_token(username):
    '''Returns a Spotify token for the given user. Modified from util.py in spotipy in order 
    to expose cache path'''
    scope = 'playlist-modify-public user-library-read'
    client_id = get_spotify_client_id()
    client_secret = get_spotify_client_secret()

    sp_oauth = oauth2.SpotifyOAuth(client_id,
                                   client_secret,
                                   REDIRECT_URI,
                                   scope=scope,
                                   cache_path=os.path.join(definitions.ROOT_DIR, '.cache-' + username))

    token_info = sp_oauth.get_cached_token()

    if not token_info:
        print('''
            User authentication requires interaction with your
            web browser. Once you enter your credentials and
            give authorization, you will be redirected to
            a url.  Paste that url you were directed to to
            complete the authorization.
        ''')
        auth_url = sp_oauth.get_authorize_url()
        try:
            webbrowser.open(auth_url)
            print("Opened %s in your browser" % auth_url)
        except:
            print("Please navigate here: %s" % auth_url)

        print()
        print()
        response = input("Enter the URL you were redirected to: ")

        print()
        print()

        code = sp_oauth.parse_response_code(response)
        token_info = sp_oauth.get_access_token(code)
    # Auth'ed API request
    if token_info:
        return token_info['access_token']
    else:
        return None
