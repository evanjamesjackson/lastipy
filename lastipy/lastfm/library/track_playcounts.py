import logging
import requests
from lastipy.lastfm.library.scrobbled_track import ScrobbledTrack

URL = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo'


def fetch_track_playcount(track, user, api_key):
    json_response = _send_request(_build_payload(track, user, api_key))
    return ScrobbledTrack(track_name=json_response['track']['name'], 
                          artist=json_response['track']['artist']['name'], 
                          playcount=json_response['track']['playcount'])

def _send_request(json_payload):
    response = requests.get(URL, params=json_payload)
    if response.ok:
        return response.json()
    else:
        response.raise_for_status()
 


def _build_payload(track, user, api_key):
    payload = {
        'username': user,
        'api_key': api_key,
        'format': 'json',
        'track': track.track_name,
        'artist': track.artist,
        'autocorrect': 1
    }
    return payload