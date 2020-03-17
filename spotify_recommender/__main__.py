#!/usr/bin/env python3.7

from configparser import ConfigParser
import argparse
from spotify_recommender import recommendations_playlist
import os
import logging
from spotify_recommender import definitions
from spotify_recommender.lastfm.library.top_tracks import fetch_top_tracks
from spotify_recommender.lastfm.recommendations.similar_tracks import fetch_similar_tracks
from spotify_recommender.lastfm.recommendations.recommendations import fetch_recommendations
from spotify_recommender.lastfm.library.recent_tracks import fetch_recent_tracks
from spotify_recommender.lastfm.library.recent_artists import fetch_recent_artists
from spotify_recommender.lastfm.recommendations.rating_calculator import calculate_ratings
from spotify_recommender.recommendations_playlist import build_recommendations_playlist


def _setup_logging():
    logs_directory = os.path.join(definitions.ROOT_DIR, 'logs')
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(logs_directory, 'spotify_recommender.log'),
        maxBytes=2 * 1024 * 1024,  # 2MB
        backupCount=25,
        encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def _setup_arg_parser():
    parser = argparse.ArgumentParser(description="Create a Spotify playlist based off recommendations from Last.fm")
    parser.add_argument('user_configs_file', type=argparse.FileType('r', encoding='UTF-8'))
    parser.add_argument('api_keys_file', type=argparse.FileType('r', encoding='UTF-8'))
    return parser


def _extract_user_configs(user_configs_file):
    config_parser = ConfigParser()
    config_parser.read(user_configs_file)
    section = 'Config'
    args.lastfm_user = config_parser[section]['LastFMUser']
    args.spotify_user = config_parser[section]['SpotifyUser']
    args.recommendation_period = config_parser[section]['RecommendationPeriod']
    args.max_recommendations_per_top_track = int(config_parser[section]['MaxRecommendationsPerTopTrack'])
    args.playlist_size = int(config_parser[section]['PlaylistSize'])
    args.playlist_name = config_parser[section]['PlaylistName']
    args.blacklisted_artists = config_parser[section]['BlacklistedArtists'].split(",")
    args.prefer_unheard_artists = _str_to_bool(config_parser[section]['PreferUnheardArtists'])
    return args


def _extract_api_keys(api_keys_file):
    config_parser = ConfigParser()
    config_parser.read(api_keys_file)
    args.lastfm_api_key = config_parser['LastFM']['API']
    spotify_section = 'Spotify'
    args.spotify_client_id_key = config_parser[spotify_section]['CLIENT_ID']
    args.spotify_client_secret_key = config_parser[spotify_section]['CLIENT_SECRET']
    return args


def _str_to_bool(to_convert):
    return to_convert == "True"


if __name__ == "__main__":
    _setup_logging()

    parser = _setup_arg_parser()
    args = parser.parse_args()

    if args.user_configs_file:
        if os.path.exists(args.user_configs_file.name):
            args = _extract_user_configs(args.user_configs_file.name)
        else:
            raise Exception("Could not find " + args.user_configs_file.name)

    if args.api_keys_file:
        if (os.path.exists(args.api_keys_file.name)):
            args = _extract_api_keys(args.api_keys_file.name)
        else:
            raise Exception("Could not find " + args.api_keys_file.name)


    build_recommendations_playlist(lastfm_user=args.lastfm_user, 
                                   lastfm_api_key=args.lastfm_api_key, 
                                   spotify_user=args.spotify_user, 
                                   spotify_client_id_key=args.spotify_client_id_key, 
                                   spotify_client_secret_key=args.spotify_client_secret_key, 
                                   recommendation_period=args.recommendation_period, 
                                   max_recommendations_per_top_track=args.max_recommendations_per_top_track,
                                   playlist_name=args.playlist_name, 
                                   playlist_size=args.playlist_size, 
                                   blacklisted_artists=args.blacklisted_artists, 
                                   prefer_unheard_artists=args.prefer_unheard_artists)
