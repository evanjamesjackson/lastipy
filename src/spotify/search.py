import logging
import spotipy
from .token import *
import json


def search(username, query):
    token = get_token(username)
    spotify = spotipy.Spotify(auth=token)
    results = spotify.search(q=query)
    logging.debug("Search results for query " + query + ": " + json.dumps(results))
    return results
