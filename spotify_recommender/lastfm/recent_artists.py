import logging, requests
from spotify_recommender.parse_keys import ApiKeysParser
from spotify_recommender.lastfm import track_convert
from spotify_recommender.lastfm.recommended_track import RecommendedTrack
from spotify_recommender.lastfm.scrobbled_artist import ScrobbledArtist

URL = 'http://ws.audioscrobbler.com/2.0/?method=library.getartists'
RESULTS_PER_PAGE_LIMIT = 200


class RecentArtistsFetcher:
    def __init__(self):
        self.config_parser = ApiKeysParser()

    def fetch(self, user):
        """Fetches tracks similar to the given track"""

        logging.info("Fetching recent artists for user " + user)
        artists = []
        page = 1
        total_pages = 1
        while page <= total_pages:
            json_response = self._send_request(self._build_json_payload(user, page))
            logging.debug("Response: " + str(json_response))
            for artist in json_response['artists']['artist']:
                artists.append(ScrobbledArtist(artist_name=artist['name'], playcount=int(artist['playcount'])))
            total_pages = int(json_response['artists']['@attr']['totalPages'])
            page = page + 1

        logging.info("Fetched recent artists " + str(artists))

        return artists

    def _send_request(self, json_payload):
        response = requests.get(URL, params=json_payload)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def _build_json_payload(self, user, page):
        api_key = self.config_parser.get_lastfm_key()
        payload = {
            'format': 'json',
            'page': page,
            'api_key': api_key,
            'limit': RESULTS_PER_PAGE_LIMIT,
            'user': user
        }
        return payload


if __name__ == "__main__":
    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    fetcher = RecentArtistsFetcher()
    fetcher.fetch('sonofjack3')
