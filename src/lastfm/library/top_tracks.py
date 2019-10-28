import logging, requests
from src.lastfm.parse_lastfm_tracks import parse_tracks
from src.lastfm.library import period
from src.parse_keys import get_lastfm_key

URL = 'http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks'


def fetch_top_tracks(user, a_period=period.OVERALL):
    """Fetches the top tracks for the given user over the given period"""

    page = 1
    top_tracks = []
    keep_fetching = True
    logging.info("Fetching top tracks for user " + user + " over period " + a_period)
    while keep_fetching:
        json_response = _send_request(_build_json_payload(user, a_period, page))
        tracks_to_be_converted = [track for track in json_response['toptracks']['track']]
        converted_tracks = parse_tracks(tracks_to_be_converted)
        
        # Filter out tracks with a playcount of 1, since those shouldn't be considered "top"
        converted_tracks = [track for track in converted_tracks if track.playcount > 1]
        
        logging.debug("Fetched " + str(converted_tracks))
        
        top_tracks = top_tracks + converted_tracks
        page = page + 1
        if not converted_tracks:
            keep_fetching = False

    logging.info(f"Fetched " + str(len(top_tracks)) + " top tracks: " + str(top_tracks))
    return top_tracks

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

