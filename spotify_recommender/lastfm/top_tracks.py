import logging, requests
from spotify_recommender.parse_api_keys import ApiKeysParser
from . import period, track_convert

URL = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks'


class TopTracksFetcher:
    def __init__(self):
        self.config_parser = ApiKeysParser()

    def fetch(self, user, a_period=period.OVERALL):
        """Fetches the top tracks for the given user over the given period"""

        page = 1
        top_tracks = []
        keep_fetching = True
        logging.info("Fetching top tracks for user " + user + " over period " + a_period)
        while keep_fetching:
            json_response = self._send_request(self._build_json_payload(user, a_period, page))
            converted_tracks = track_convert.convert_tracks(json_response['toptracks']['track'])
            logging.debug("Fetched " + str(converted_tracks))
            top_tracks = top_tracks + converted_tracks
            page = page + 1
            if not converted_tracks:
                keep_fetching = False

        logging.info(f"Fetched " + str(len(top_tracks)) + " top tracks: " + str(top_tracks))
        return top_tracks

    def _send_request(self, json_payload):
        response = requests.get(URL, params=json_payload)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def _build_json_payload(self, user, period, page):
        api_key = self.config_parser.get_lastfm_key()
        payload = {
            'user': user,
            'api_key': api_key,
            'format': 'json',
            'period': period,
            'page': page
        }
        return payload

