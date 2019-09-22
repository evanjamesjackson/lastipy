import logging
import spotipy
from src.spotify import token
from src.spotify import track_convert
import json


def search_for_tracks(username, query):
    """Returns a list of tracks for the given query"""

    spotify = spotipy.Spotify(auth=token.get_token(username))
    results = spotify.search(q=query)
    logging.debug("All search results for query " + query + ": " + json.dumps(results))

    converted_tracks = []
    if results['tracks']:
        converted_tracks = track_convert.convert_json_tracks(results['tracks']['items'])
    logging.info("Track results for query " + query + ": " + str(converted_tracks))
    return converted_tracks
