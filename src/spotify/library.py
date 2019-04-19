from src.spotify.token import *
import spotipy
import logging


def get_tracks_in_playlists(username):
    """Returns the IDs of all the tracks in the given user's playlists"""

    logging.info("Fetching all tracks in " + username + "'s playlists")

    spotify = spotipy.Spotify(auth=get_token(username))

    playlists = spotify.current_user_playlists()['items']

    track_ids = []
    for playlist in playlists:
        track_ids = track_ids + _get_tracks_in_playlist(spotify, username, playlist)

    return track_ids


def _get_tracks_in_playlist(spotify, username, playlist):
    track_ids_in_playlist = []

    keep_fetching = True
    while keep_fetching:
        tracks = spotify.user_playlist_tracks(user=username,
                                              playlist_id=playlist['id'],
                                              offset=len(track_ids_in_playlist))['items']
        if tracks:
            track_ids_in_playlist = track_ids_in_playlist + [_get_track_id(track) for track in tracks]
        else:
            keep_fetching = False

    return track_ids_in_playlist


def get_saved_tracks(username):
    """Returns the IDs of all the given user's saved tracks"""

    logging.info("Fetching " + username + "'s saved tracks")

    spotify = spotipy.Spotify(auth=get_token(username))

    track_ids = []
    keep_fetching = True
    while keep_fetching:
        tracks = spotify.current_user_saved_tracks(offset=len(track_ids))['items']
        if tracks:
            track_ids = track_ids + [_get_track_id(track) for track in tracks]
        else:
            keep_fetching = False

    return track_ids


def _get_track_id(track):
    return track['track']['id']


