import logging


#TODO test
def replace_tracks_in_playlist(spotify, username, playlist_name, tracks):
    """Replaces all tracks in given user's given playlist with the given tracks. 
        If the playlist does not exist, creates it first."""

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

def add_tracks_to_playlist(spotify, username, playlist_name, tracks):
    """Adds all the given tracks to the given user's given playlist. 
        If the playlist does not exist, creates it first."""

    playlists = spotify.current_user_playlists()
    playlists = [playlist for playlist in playlists['items'] if playlist['name'] == playlist_name]
    if playlists:
        playlist_id = playlists[0]['id']
    else:
        logging.info("Creating playlist " + playlist_name)
        playlist_id = spotify.user_playlist_create(user=spotify.current_user()['id'], name=playlist_name)['id']

    logging.info("Adding " + str(len(tracks)) + " tracks to " + username + "'s playlist " + playlist_name + ": " + str(tracks))

    # Spotify only allows 100 tracks to be added to a playlist at once
    track_chunks = [tracks[i:i + 100] for i in range(0, len(tracks), 100)]  
    for chunk in track_chunks:
        spotify.user_playlist_add_tracks(user=spotify.current_user()['id'],
                                         playlist_id=playlist_id,
                                         tracks=[track.spotify_id for track in chunk])
