from src.track import Track
from src.lastfm.library.scrobbled_track import ScrobbledTrack


def parse_tracks(json_tracks):
    converted_tracks = []
    for track in json_tracks:
        converted_tracks.append(_parse_track(track))
    return converted_tracks


def _parse_track(json_track):
    track_name = json_track['name']

    artist_json = json_track['artist']
    if 'name' in artist_json:
        artist = artist_json['name']
    elif '#text' in artist_json:
        artist = artist_json['#text']

    if 'playcount' in json_track:
        # TODO kinda smelly having this here
        return ScrobbledTrack(track_name, artist, int(json_track['playcount']))

    return Track(track_name, artist)
