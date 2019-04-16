import logging, requests
from .parse_api_keys import ApiKeysParser
from .track import Track
from . import period, track_convert

URL = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks'

RESULTS_PER_PAGE_LIMIT = 200

class RecentTracksFetcher:
    def __init__(self):
        self.config_parser = ApiKeysParser()

    def fetch(self, user):
        """Fetches recent tracks for the given user"""

        page = 1
        recent_tracks = []
        keep_fetching = True
        logging.info("Fetching recent tracks for " + user + "...")
        while keep_fetching:
            json_response = self.__send_request(self.__build_json_payload(user, page))
            converted_tracks = track_convert.convert_tracks(json_response['recenttracks']['track'])
            logging.debug("Fetched " + str(converted_tracks))
            recent_tracks = recent_tracks + converted_tracks
            page = page + 1
            if not converted_tracks:
                keep_fetching = False

        logging.info("Fetched recent tracks: " + str(recent_tracks))
        return recent_tracks

    def __send_request(self, json_payload):
        response = requests.get(URL, params=json_payload)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def __build_json_payload(self, user, page):
        api_key = self.config_parser.get_lastfm_key()
        payload = {
            'user': user,
            'format': 'json',
            'api_key': api_key,
            'limit': RESULTS_PER_PAGE_LIMIT,
            'page': page
        }
        return payload