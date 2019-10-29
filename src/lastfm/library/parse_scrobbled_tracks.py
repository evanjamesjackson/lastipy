from src.lastfm.parse_lastfm_tracks import parse_track_name, parse_artist
from src.lastfm.library.scrobbled_track import ScrobbledTrack

#TODO only use this for top tracks, not recents (no playcount)
def parse_scrobbled_tracks(json_tracks):
    scrobbled_tracks = []
    for json_track in json_tracks:
        track_name = parse_track_name(json_track)
        artist = parse_artist(json_track)
        playcount = int(json_track['playcount']) if ('playcount' in json_track) else 0
        scrobbled_tracks.append(ScrobbledTrack(track_name=track_name, artist=artist, playcount=playcount))
    return scrobbled_tracks
