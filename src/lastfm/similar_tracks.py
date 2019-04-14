import requests
from .parse_api_keys import ApiKeysParser
from .track import Track
from . import period, track_convert

URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getsimilar'

class SimilarTracksFetcher:
    def __init__(self):
        self.config_parser = ApiKeysParser()
        
    def fetch_similar_tracks(self, track, limit):
        """Fetches tracks similar to the given track"""
        
        json_payload = self.__buildJsonPayload(track, limit)
        json_response = self.__send_request(json_payload)
        if ('similartracks' in json_response):
            return track_convert.convert_tracks(json_response['similartracks']['track'])    
        elif ('errors' in json_response):
            raise Exception("Error occurred while fetching similar tracks " + json_response['errors'])

    def __send_request(self, json_payload):
        response = requests.get(URL, params=json_payload)
        if (response.ok):
            return response.json()
        else:
            response.raise_for_status()

    def __buildJsonPayload(self, track, limit):
        api_key = self.config_parser.get_lastfm_key()
        payload = {
            'track' : track.track_name,
            'artist' : track.artist,
            'format' : 'json',
            'api_key' : api_key,
            'limit' : limit
        }
        return payload
