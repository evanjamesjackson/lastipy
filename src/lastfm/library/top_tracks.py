import logging, requests
from src.lastfm.library import period
from src.parse_keys import get_lastfm_key
from src.lastfm.library.parse_scrobbled_tracks import parse_scrobbled_tracks

URL = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks'


def fetch_top_tracks(user, a_period=period.OVERALL):
    """Fetches the top tracks for the given user over the given period"""

    page = 1
    all_top_tracks = []
    keep_fetching = True
    logging.info("Fetching top tracks for user " + user + " over period " + a_period)
    while keep_fetching:
        json_response = _send_request(_build_json_payload(user, a_period, page))
        json_tracks = [track for track in json_response['toptracks']['track']]
        top_tracks = parse_scrobbled_tracks(json_tracks)
        
        # Filter out tracks with a playcount of 1, since those shouldn't be considered "top"
        top_tracks = [track for track in top_tracks if track.playcount > 1]
        
        logging.debug("Fetched " + str(top_tracks))
        
        all_top_tracks = all_top_tracks + top_tracks
        page = page + 1
        if not top_tracks:
            keep_fetching = False

    logging.info(f"Fetched " + str(len(all_top_tracks)) + " top tracks: " + str(all_top_tracks))
    return all_top_tracks

def _send_request(json_payload):
    response = requests.get(URL, params=json_payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()

def _build_json_payload(user, period, page):
    api_key = get_lastfm_key()
    payload = {
        'user': user,
        'api_key': api_key,
        'format': 'json',
        'period': period,
        'page': page
    }
    return payload

