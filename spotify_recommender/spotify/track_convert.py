from ..spotify.spotify_track import SpotifyTrack


def convert_json_tracks(json_tracks):
    return [convert_json_track(json_track) for json_track in json_tracks]


def convert_json_track(json_track):
    # Just getting the first artist, even if there's multiple
    if 'track' in json_track:
        # Some endpoints do this, others don't
        json_track = json_track['track']
    artist = json_track['artists'][0]['name']
    name = json_track['name']
    track_id = json_track['id']
    return SpotifyTrack(track_name=name, artist=artist, spotify_id=track_id)
