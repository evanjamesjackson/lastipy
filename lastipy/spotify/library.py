from lastipy.spotify.parse_spotify_tracks import parse_tracks
import spotipy
import logging


#TODO test
def get_tracks_in_playlists(spotify, username):
    """Returns all tracks in the given user's playlists"""

    logging.info("Fetching all tracks in " + username + "'s playlists")

    playlists = spotify.current_user_playlists()['items']

    tracks = []
    for playlist in playlists:
        tracks = tracks + get_tracks_in_playlist(spotify, username, playlist['id'])

    logging.info("Fetched tracks " + str(tracks))

    return tracks

def get_tracks_in_playlist(spotify, username, playlist_name=None, playlist_id=None):
    if playlist_id == None:
        if playlist_name == None:
            raise Exception("Playlist ID or playlist name required")
        playlists = spotify.current_user_playlists()
        matching_playlists = [playlist for playlist in playlists['items'] if playlist['name'] == playlist_name]
        if not matching_playlists:
            logging.warn("No playlist with name " + playlist_name + " found for user " + username)
            return []
        else:
            playlist_id = matching_playlists[0]['id']

    tracks_in_playlist = []

    keep_fetching = True
    while keep_fetching:
        json_response = spotify.user_playlist_tracks(user=username,
                                                   playlist_id=playlist_id,
                                                   offset=len(tracks_in_playlist))
        if json_response['items']:
            tracks_in_playlist = tracks_in_playlist + parse_tracks(json_response['items'])
        else:
            keep_fetching = False

    return tracks_in_playlist


def get_saved_tracks(spotify, username):
    """Returns the all of the given user's saved tracks"""

    logging.info("Fetching " + username + "'s saved tracks")

    saved_tracks = []
    keep_fetching = True
    while keep_fetching:
        json_response = spotify.current_user_saved_tracks(offset=len(saved_tracks))
        if json_response['items']:
            saved_tracks = saved_tracks + parse_tracks(json_response['items'])
        else:
            keep_fetching = False

    logging.info("Fetched tracks " + str(saved_tracks))

    return saved_tracks

def add_tracks_to_library(spotify, tracks):
    logging.info("Adding " + str(tracks) + " to library")
    # Spotify only allows 50 tracks to be added to a library at once, so we need to chunk 'em up
    track_chunks = [tracks[i:i + 50] for i in range(0, len(tracks), 50)]  
    for chunk in track_chunks:
        spotify.current_user_saved_tracks_add([track.spotify_id for track in chunk])