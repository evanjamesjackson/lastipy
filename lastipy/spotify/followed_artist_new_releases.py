import spotipy
from lastipy.spotify.parse_spotify_tracks import parse_tracks
from datetime import datetime


def get_tracks_from_followed_artists(spotify, as_of_date):
    followed_artists = []

    curr_response = spotify.current_user_followed_artists(limit=50)

    while len(curr_response['artists']['items']) > 0:
        curr_response = spotify.current_user_followed_artists(limit=50, after=curr_response['artists']['items'][len(curr_response) - 1]['id'])
        followed_artists += curr_response['artists']['items']

    # The above Spotipy function doesn't really function properly and results in duplicates, 
    # so we remove them here by converting the list to just the IDs (not doing so results in
    # an unhashable error), then converting to a set and back to a list 
    followed_artists = [artist['id'] for artist in followed_artists]
    followed_artist_ids = list(set(followed_artists))

    all_albums = []
    for artist_id in followed_artist_ids:
        curr_response = spotify.artist_albums(artist_id, album_type='album', limit=50)
        artist_albums = curr_response['items']
        while len(curr_response['items']) > 0:
            curr_response = spotify.artist_albums(artist_id, album_type='album', limit=50, offset=len(artist_albums))
            artist_albums += curr_response['items']
        all_albums += artist_albums

    new_albums = []
    for album in all_albums:
        if album['release_date_precision'] == 'day':
            if datetime.strptime(album['release_date'], "%Y-%m-%d").date() >= as_of_date:
                new_albums.append(album)
        elif album['release_date_precision'] == 'month':
            release_date = datetime.strptime(album['release_date'], "%Y-%m")
            if release_date.year > as_of_date.year or (release_date.year == as_of_date.year and release_date.month >= as_of_date.month):
                   new_albums.append(album)
        elif album['release_date_precision'] == 'year':
            if datetime.strptime(album['release_date'], '%Y').year >= as_of_date.year:
                new_albums.append(album)

    all_tracks = []
    for album in new_albums:
        curr_response = spotify.album_tracks(album['id'], limit=50)
        album_tracks = curr_response['items']
        while len(curr_response['items']) > 0:
            curr_response = spotify.album_tracks(album['id'], limit=50, offset=len(album_tracks))
            album_tracks += curr_response['items']
        all_tracks += album_tracks

    return parse_tracks(all_tracks)
