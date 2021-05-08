import logging
import requests
from lastipy.lastfm.library.scrobbled_artist import ScrobbledArtist
from lastipy.lastfm.library.paginated_endpoint import fetch_paginated_response

URL = 'http://ws.audioscrobbler.com/2.0/?method=library.getartists'


def fetch_recent_artists(user, api_key):
    """Fetches recent artists for the given user"""

    logging.info("Fetching recent artists for user " + user)

    paginated_json_responses = fetch_paginated_response(
        URL, user, api_key, 'artists')

    artists = []
    for json_response in paginated_json_responses:
        for artist in json_response['artists']['artist']:
            artists.append(ScrobbledArtist(
                artist_name=artist['name'], playcount=int(artist['playcount'])))

    logging.info("Fetched " + str(len(artists)) + " artists")
    logging.debug("Fetched artists: " + str(artists))

    return artists
