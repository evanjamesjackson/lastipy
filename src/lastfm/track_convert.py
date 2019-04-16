from .track import Track

def convert_tracks(tracks_to_convert):
    """Converts the given list of LastFM-formatted tracks into Track objects"""
    converted_tracks = []
    for track in tracks_to_convert:
        converted_tracks.append(__convert_track(track))
    return converted_tracks
    
def __convert_track(track_to_convert):
    track_name = track_to_convert['name']

    artist_json = track_to_convert['artist']
    if 'name' in artist_json:
        artist = artist_json['name']
    elif '#text' in artist_json:
        artist = artist_json['#text']

    return Track(track_name, artist)