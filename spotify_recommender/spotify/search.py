import logging
import spotipy
from .token import *
import json


def search_for_tracks(username, query):
    """Returns a list of track IDs for the given query"""

    token = get_token(username)
    spotify = spotipy.Spotify(auth=token)
    results = spotify.search(q=query)
    logging.debug("Search results for query " + query + ": " + json.dumps(results))
    return _extract_ids(results)


def _extract_ids(results):
    track_ids = []
    if results['tracks']['items']:
        track_ids.append(results['tracks']['items'][0]['id'])
    return track_ids
