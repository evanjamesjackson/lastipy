from src.spotify import token
from src.spotify import track_convert
import spotipy
import logging


#TODO test
def get_tracks_in_playlists(username):
    """Returns all tracks in the given user's playlists"""

    logging.info("Fetching all tracks in " + username + "'s playlists")

    spotify = spotipy.Spotify(auth=token.get_token(username))

    playlists = spotify.current_user_playlists()['items']

    tracks = []
    for playlist in playlists:
        tracks = tracks + _get_tracks_in_playlist(spotify, username, playlist)

    logging.info("Fetched tracks " + str(tracks))

    return tracks


def _get_tracks_in_playlist(spotify, username, playlist):
    tracks_in_playlist = []

    keep_fetching = True
    while keep_fetching:
        json_tracks = spotify.user_playlist_tracks(user=username,
                                                   playlist_id=playlist['id'],
                                                   offset=len(tracks_in_playlist))
        if json_tracks['items']:
            tracks_in_playlist = tracks_in_playlist + track_convert.convert_json_tracks(json_tracks['items'])
        else:
            keep_fetching = False

    return tracks_in_playlist


def get_saved_tracks(username):
    """Returns the all of the given user's saved tracks"""

    logging.info("Fetching " + username + "'s saved tracks")

    spotify = spotipy.Spotify(auth=token.get_token(username))

    saved_tracks = []
    keep_fetching = True
    while keep_fetching:
        json_tracks = spotify.current_user_saved_tracks(offset=len(saved_tracks))
        if json_tracks['items']:
            saved_tracks = saved_tracks + track_convert.convert_json_tracks(json_tracks['items'])
        else:
            keep_fetching = False

    logging.info("Fetched tracks " + str(saved_tracks))

    return saved_tracks
