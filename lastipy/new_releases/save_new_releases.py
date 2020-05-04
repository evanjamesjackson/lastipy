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
from lastipy.spotify.new_followed_artist_releases import fetch_new_releases
from datetime import datetime
from lastipy.lastfm.library.recent_tracks import fetch_recent_tracks


def save_new_releases():
    """Saves new releases (as of the current date) from the specified Spotify user's followed artists to their library"""

    setup_logging('new_releases.log')
    args = _extract_args()

    spotify = Spotify(auth=token.get_token(args.spotify_user, args.spotify_client_id_key, args.spotify_client_secret_key))

    new_tracks = fetch_new_releases(spotify=spotify)

    if len(new_tracks) > 0:
        # Only process further if we actually fetched any new tracks; otherwise there's no point

        # Filter out new tracks that are already saved in the library        
        saved_tracks = library.get_saved_tracks(username=args.spotify_user, spotify=spotify)
        tracks_to_save = [new_track for new_track in new_tracks 
                            if not any(new_track == saved_track for saved_track in saved_tracks)]
        
        library.add_tracks_to_library(spotify, tracks_to_save)
    else:
        logging.info("No new tracks to add!")

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
    save_new_releases()