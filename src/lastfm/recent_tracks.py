import logging, requests
from src.parse_api_keys import ApiKeysParser
from . import track_convert

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
        max_retries = 3
        retries = 0
        while keep_fetching:
            try:
                json_response = self._send_request(self._build_json_payload(user, page))
                converted_tracks = track_convert.convert_tracks(json_response['recenttracks']['track'])
                logging.debug("Fetched " + str(converted_tracks))
                recent_tracks = recent_tracks + converted_tracks
                page = page + 1
                if not converted_tracks:
                    keep_fetching = False
            except Exception as e:
                # This particular endpoint has a habit of throwing back error 500, so just retry if it does
                if retries < max_retries:
                    retries = retries + 1
                else:
                    raise e

        logging.info(f"Fetched " + str(len(recent_tracks)) + " recent tracks: " + str(recent_tracks))
        return recent_tracks

    def _send_request(self, json_payload):
        response = requests.get(URL, params=json_payload)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def _build_json_payload(self, user, page):
        api_key = self.config_parser.get_lastfm_key()
        payload = {
            'user': user,
            'format': 'json',
            'api_key': api_key,
            'limit': RESULTS_PER_PAGE_LIMIT,
            'page': page
        }
        return payload