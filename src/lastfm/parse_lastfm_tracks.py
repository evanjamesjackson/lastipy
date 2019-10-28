from src.track import Track
from src.lastfm.library.scrobbled_track import ScrobbledTrack


def parse_tracks(json_tracks):
    return [_parse_track(json_track) for json_track in json_tracks]

def _parse_track(json_track):
    track_name = json_track['name']

    artist_json = json_track['artist']
    if 'name' in artist_json:
        artist = artist_json['name']
    elif '#text' in artist_json:
        artist = artist_json['#text']

    if 'playcount' in json_track:
        # If a playcount exists, this is a track that's been scrobbled so we'll return that instead of 
        # a regular Track object
        return ScrobbledTrack(track_name, artist, int(json_track['playcount']))
    else:
        return Track(track_name, artist)
