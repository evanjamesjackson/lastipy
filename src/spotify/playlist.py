import logging
import spotipy
from src.spotify import token


#TODO test
def add_to_playlist(username, playlist_name, tracks):
    """Adds the given tracks to the given user's given playlist. If the playlist does not exist, creates it first"""

    spotify = spotipy.Spotify(auth=token.get_token(username))

    playlists = spotify.current_user_playlists()
    playlists = [playlist for playlist in playlists['items'] if playlist['name'] == playlist_name]
    if playlists:
        playlist_id = playlists[0]['id']
    else:
        logging.info("Creating playlist " + playlist_name)
        playlist_id = spotify.user_playlist_create(user=spotify.current_user()['id'], name=playlist_name)['id']

    logging.info("Adding " + str(len(tracks)) + " tracks to " + username + "'s playlist " + playlist_name + ": " + str(tracks))

    spotify.user_playlist_replace_tracks(user=spotify.current_user()['id'],
                                         playlist_id=playlist_id,
                                         tracks=[track.spotify_id for track in tracks])
