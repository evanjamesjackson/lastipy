import logging, requests
from ..parse_keys import ApiKeysParser
from . import track_convert

URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar'


class SimilarTracksFetcher:
    def __init__(self):
        self.config_parser = ApiKeysParser()
        
    def fetch(self, track, limit):
        """Fetches tracks similar to the given track"""

        logging.info("Fetching up to " + str(limit) + " tracks similar to " + str(track))
        json_response = self._send_request(self._build_json_payload(track, limit))
        if 'similartracks' in json_response:
            similar_tracks = track_convert.convert_tracks(json_response['similartracks']['track'])
            logging.info(f"Fetched " + str(len(similar_tracks)) + " similar tracks: " + str(similar_tracks))
            return similar_tracks
        elif 'errors' in json_response:
            raise Exception("Error occurred while fetching similar tracks " + json_response['errors'])

    def _send_request(self, json_payload):
        response = requests.get(URL, params=json_payload)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def _build_json_payload(self, track, limit):
        api_key = self.config_parser.get_lastfm_key()
        payload = {
            'track': track.track_name,
            'artist': track.artist,
            'format': 'json',
            'api_key': api_key,
            'limit': limit
        }
        return payload
