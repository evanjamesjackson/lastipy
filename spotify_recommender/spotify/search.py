import logging
import spotipy
from . import token
from . import track_convert


def search_for_tracks(username, query):
    """Returns a list of track IDs for the given query"""

    spotify = spotipy.Spotify(auth=token.get_token(username))
    results = spotify.search(q=query)
    converted_tracks = []
    if results['tracks']:
        converted_tracks = track_convert.convert_json_tracks(results['tracks']['items'])
    logging.info("Track results for query " + query + ": " + str(converted_tracks))
    return converted_tracks
