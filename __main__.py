#!/usr/bin/env python3.7

from configparser import ConfigParser
import argparse
from src import recommendations_playlist
import os
import logging
from src import definitions
from src.lastfm.library.top_tracks import fetch_top_tracks
from src.lastfm.recommendations.similar_tracks import fetch_similar_tracks
from src.lastfm.recommendations.recommendations import fetch_recommendations
from src.lastfm.library.recent_tracks import fetch_recent_tracks
from src.lastfm.library.recent_artists import fetch_recent_artists
from src.lastfm.recommendations.rating_calculator import calculate_ratings
from src.recommendations_playlist import build_recommendations_playlist


def _setup_logging():
    logs_directory = os.path.join(definitions.ROOT_DIR, 'logs')
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Instantiating with the name __package__ works because this file is in the topmost package
    logger = logging.getLogger(__package__)
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
    parser.add_argument('file', type=argparse.FileType('r', encoding='UTF-8'))
    return parser


def _extract_args_from_file(args):
    config_parser = ConfigParser()
    config_parser.read(args.file.name)
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


def _str_to_bool(to_convert):
    return to_convert == "True"


if __name__ == "__main__":
    _setup_logging()

    parser = _setup_arg_parser()
    args = parser.parse_args()

    if args.file:
        if os.path.exists(args.file.name):
            args = _extract_args_from_file(args)
        else:
            raise Exception("Could not find " + args.file.name)


    build_recommendations_playlist(args.lastfm_user,
                                   args.spotify_user,
                                   args.recommendation_period,
                                   args.max_recommendations_per_top_track,
                                   args.playlist_name,
                                   args.playlist_size,
                                   args.blacklisted_artists,
                                   args.prefer_unheard_artists)
