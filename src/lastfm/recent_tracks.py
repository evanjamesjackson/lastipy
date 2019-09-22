import logging
import requests
from src.parse_keys import ApiKeysParser
from src.lastfm import track_convert
from requests import RequestException

URL = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks'
RESULTS_PER_PAGE_LIMIT = 200
MAX_RETRIES = 10


class RecentTracksFetcher:
    def __init__(self):
        self.config_parser = ApiKeysParser()

    def fetch(self, user):
        """Fetches recent tracks for the given user"""

        logging.info("Fetching recent tracks for " + user + "...")
        recent_tracks = []
        page = 1
        total_pages = 1
        retries = 0
        while page <= total_pages:
            try:
                json_response = self._send_request(self._build_json_payload(user, page))
                logging.debug("Response: " + str(json_response))
                converted_tracks = track_convert.convert_tracks(json_response['recenttracks']['track'])
                recent_tracks = recent_tracks + converted_tracks
                total_pages = int(json_response['recenttracks']['@attr']['totalPages'])
                page = page + 1
            except RequestException:
                # This particular endpoint has a habit of throwing back error 500, so just retry if it does
                if retries < MAX_RETRIES:
                    logging.warning("Failed to fetch recent tracks page " + str(page) + ". Retrying...")
                    retries = retries + 1
                else:
                    logging.warning("Failed to fetch recent tracks page " + str(page) +
                                    " after " + str(retries) + " retries. Giving up and moving on...")
                    break

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
