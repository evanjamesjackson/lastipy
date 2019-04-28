import logging
import spotipy
from . import token
import json


def add_to_playlist(username, playlist_name, track_ids):
    """Adds the given tracks to the given user's given playlist. If the playlist does not exist, creates it first"""

    spotify = spotipy.Spotify(auth=token.get_token(username))

    playlists = spotify.current_user_playlists()
    playlists = [playlist for playlist in playlists['items'] if playlist['name'] == playlist_name]
    if playlists:
        playlist_id = playlists[0]['id']
    else:
        logging.info("Creating playlist " + playlist_name)
        playlist_id = spotify.user_playlist_create(user=spotify.current_user()['id'], name=playlist_name)['id']

    logging.info("Adding tracks to playlist " + playlist_name + ": " + json.dumps(track_ids))

    spotify.user_playlist_replace_tracks(spotify.current_user()['id'], playlist_id=playlist_id, tracks=track_ids)
