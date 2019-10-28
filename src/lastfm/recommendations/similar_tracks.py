import logging
import requests
from src.parse_keys import get_lastfm_key
from src.lastfm.parse_lastfm_tracks import parse_tracks
from src.lastfm.recommendations.recommended_track import RecommendedTrack

URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar'


def fetch_similar_tracks(track, limit):
    """Fetches tracks similar to the given track"""

    logging.info("Fetching up to " + str(limit) + " tracks similar to " + str(track))
    json_response = _send_request(_build_json_payload(track, limit))
    if 'similartracks' in json_response:
        similar_tracks = parse_tracks(json_response['similartracks']['track'])
        similar_tracks = list(map(lambda similar_track: RecommendedTrack(similar_track.track_name,
                                                                    similar_track.artist,
                                                                    track.playcount),
                                similar_tracks))
        logging.info(f"Fetched " + str(len(similar_tracks)) + " similar tracks: " + str(similar_tracks))
        return similar_tracks
    elif 'errors' in json_response:
        raise Exception("Error occurred while fetching similar tracks " + json_response['errors'])

def _send_request(json_payload):
    response = requests.get(URL, params=json_payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def _build_json_payload(track, limit):
    api_key = get_lastfm_key()
    payload = {
        'track': track.track_name,
        'artist': track.artist,
        'format': 'json',
        'api_key': api_key,
        'limit': limit
    }
    return payload
