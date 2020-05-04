#!/usr/bin/env python3.7

from configparser import ConfigParser
import argparse
import os
from lastipy import definitions
from lastipy.lastfm.library.top_tracks import fetch_top_tracks
from lastipy.lastfm.recommendations.similar_tracks import fetch_similar_tracks
from lastipy.recommendations.fetch_recommendations import fetch_recommendations
from lastipy.lastfm.library.recent_tracks import fetch_recent_tracks
from lastipy.lastfm.library.recent_artists import fetch_recent_artists
from lastipy.lastfm.library import period
from lastipy.spotify import library, playlist, search
from lastipy.track import Track
from numpy.random import choice
from spotipy import Spotify
from lastipy.spotify import token
from lastipy.util.setup_logging import setup_logging
import logging
from lastipy.spotify.followed_artist_new_releases import get_tracks_from_followed_artists
from datetime import datetime
from lastipy.lastfm.library.recent_tracks import fetch_recent_tracks


def build_new_releases_playlist():
    setup_logging('new_releases.log')
    args = _extract_args()

    spotify = Spotify(auth=token.get_token(args.spotify_user, args.spotify_client_id_key, args.spotify_client_secret_key))

    new_tracks = get_tracks_from_followed_artists(spotify=spotify, as_of_date=datetime(year=2019, month=1, day=1).date())
    
    library_saved_tracks = library.get_saved_tracks(username=args.spotify_user, spotify=spotify)
    library_playlist_tracks = library.get_tracks_in_playlists(username=args.spotify_user, spotify=spotify)
    scrobbled_tracks = fetch_recent_tracks(user=args.lastfm_user, api_key=args.lastfm_api_key)

    tracks_for_playlist = []

    # Get tracks already in the playlist (if there are any) and filter out any that have been scrobbled
    tracks_in_playlist = library.get_tracks_in_playlist(spotify=spotify, username=args.spotify_user, playlist_name=args.playlist_name)
    logging.debug("Tracks already in playlist before removing those that are scrobbled: " + str(tracks_in_playlist))
    tracks_in_playlist = [track for track in tracks_in_playlist
                            if not any(Track.are_equivalent(track, scrobbled_track)
                                for scrobbled_track in scrobbled_tracks)]
    logging.debug("Tracks already in playlist after filtering: " + str(tracks_in_playlist))

    tracks_for_playlist = tracks_in_playlist

    for track in new_tracks:
        if track not in library_saved_tracks \
            and track not in library_playlist_tracks \
            and not any(Track.are_equivalent(track, scrobbled_track) for scrobbled_track in scrobbled_tracks):
                logging.debug("Adding " + str(track) + " to list")
                tracks_for_playlist.append(track)
    
    logging.debug("Tracks to be added: " + str(tracks_for_playlist))

    playlist.add_tracks_to_playlist(spotify, args.spotify_user, args.playlist_name, tracks_for_playlist)

    logging.info("Done!")

def _extract_args():
    args = _setup_arg_parser().parse_args()

    if args.user_configs_file:
        if os.path.exists(args.user_configs_file.name,):
            args = _extract_user_configs(args.user_configs_file.name, args)
        else:
            raise Exception("Could not find " + args.user_configs_file.name)

    if args.api_keys_file:
        if (os.path.exists(args.api_keys_file.name)):
            args = _extract_api_keys(args.api_keys_file.name, args)
        else:
            raise Exception("Could not find " + args.api_keys_file.name)
    
    return args

def _setup_arg_parser():
    parser = argparse.ArgumentParser(description="Adds new tracks from followed artists to a Spotify playlist")
    parser.add_argument('user_configs_file', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('api_keys_file', type=argparse.FileType('r', encoding='UTF-8'))
    return parser

def _extract_user_configs(user_configs_file, args):
    config_parser = ConfigParser()
    config_parser.read(user_configs_file)
    section = 'Config'
    args.lastfm_user = config_parser[section]['LastFMUser']
    args.spotify_user = config_parser[section]['SpotifyUser']
    args.playlist_name = config_parser[section]['PlaylistName']
    return args

def _extract_api_keys(api_keys_file, args):
    config_parser = ConfigParser()
    config_parser.read(api_keys_file)
    args.lastfm_api_key = config_parser['LastFM']['API']
    spotify_section = 'Spotify'
    args.spotify_client_id_key = config_parser[spotify_section]['CLIENT_ID']
    args.spotify_client_secret_key = config_parser[spotify_section]['CLIENT_SECRET']
    return args

if __name__ == "__main__":
    build_new_releases_playlist()