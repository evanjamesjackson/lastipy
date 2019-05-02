import logging
import spotipy
from . import token
import json
from ..track import Track


def search_for_tracks(username, query):
    """Returns a list of track IDs for the given query"""

    spotify = spotipy.Spotify(auth=token.get_token(username))
    results = spotify.search(q=query)
    converted_tracks = _convert_json_results_to_tracks(results)
    logging.info("Track results for query " + query + ": " + str(converted_tracks))
    return converted_tracks


def _convert_json_results_to_tracks(results):
    converted_tracks = []
    json_tracks = [track for track in results['tracks']['items']]
    for json_track in json_tracks:
        # Just getting the first artist, in case there are multiple
        artist = json_track['artists'][0]['name']
        name = json_track['name']
        track_id = json_track['id']
        converted_tracks.append(Track(track_name=name, artist=artist, spotify_id=track_id))
    return converted_tracks
