from spotify_recommender.track import Track


def convert_tracks(tracks_to_convert):
    """Converts the given list of Last.fm-formatted tracks into Track objects"""
    converted_tracks = []
    for track in tracks_to_convert:
        converted_tracks.append(_convert_track(track))
    return converted_tracks


def _convert_track(track_to_convert):
    track_name = track_to_convert['name']

    artist_json = track_to_convert['artist']
    if 'name' in artist_json:
        artist = artist_json['name']
    elif '#text' in artist_json:
        artist = artist_json['#text']

    if 'playcount' in track_to_convert:
        playcount = track_to_convert['playcount']
    else:
        playcount = 1

    return Track(track_name, artist, playcount)
