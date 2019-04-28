import logging, requests
from ..parse_keys import ApiKeysParser
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
            # Filter out tracks whose playcount <= 1, since those shouldn't be considered "top"
            tracks_to_be_converted = [track for track
                                      in json_response['toptracks']['track']
                                      if int(track['playcount']) > 1]
            converted_tracks = track_convert.convert_tracks(tracks_to_be_converted)
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

