#!/usr/bin/env python3.7

import argparse
import logging
import logging.handlers
from spotify_recommender.lastfm import period
from spotify_recommender.lastfm.top_tracks import TopTracksFetcher
from spotify_recommender.lastfm.similar_tracks import SimilarTracksFetcher
from spotify_recommender.lastfm.top_recommendations import TopRecommendationsFetcher
from spotify_recommender.lastfm.recent_tracks import RecentTracksFetcher
from spotify_recommender.spotify import library, playlist, search
from configparser import ConfigParser
import os
from spotify_recommender import definitions
from spotify_recommender.track import Track
from numpy.random import choice


PLAYLIST_NAME = "Last.fm"


def create_recommendations_playlist(lastfm_user,
                                    spotify_user,
                                    recommendation_period=period.OVERALL,
                                    max_recommendations_per_top_track=50,
                                    playlist_size=40):

    recommendations_fetcher = TopRecommendationsFetcher(similar_fetcher=SimilarTracksFetcher(),
                                                        top_fetcher=TopTracksFetcher(),
                                                        recent_fetcher=RecentTracksFetcher())
    recommendations = recommendations_fetcher.fetch(user=lastfm_user,
                                                    recommendation_period=recommendation_period,
                                                    max_similar_tracks_per_top_track=max_recommendations_per_top_track)

    saved_tracks = library.get_saved_tracks(spotify_user)
    playlist_tracks = library.get_tracks_in_playlists(spotify_user)

    weights = _get_weights(recommendations)
    tracks_for_playlist = []
    while len(tracks_for_playlist) < playlist_size:
        recommendation = choice(recommendations, p=weights)
        search_results = search.search_for_tracks(username=spotify_user,
                                                  query=recommendation.artist + " " + recommendation.track_name)
        first_result = search_results[0] if search_results else None

        first_result = first_result \
            if first_result is not None \
            and Track.are_equivalent(first_result, recommendation) \
            and first_result not in playlist_tracks \
            and first_result not in saved_tracks \
            else None
        if first_result is not None:
            tracks_for_playlist.append(search_results[0])

    playlist.add_to_playlist(spotify_user, PLAYLIST_NAME, tracks_for_playlist)


def _get_weights(recommendations):
    ratings = [recommendation.recommendation_rating for recommendation in recommendations]
    ratings_total = sum(ratings)
    logging.debug(f"Ratings total: " + str(ratings_total))
    weights = [recommendation.recommendation_rating / ratings_total for recommendation in recommendations]
    logging.debug(f"Weights: " + str(weights))
    return weights


def _main():
    _setup_logging()

    parser = _setup_arg_parser()
    args = parser.parse_args()

    if args.file:
        if os.path.exists(args.file.name):
            args = _extract_args_from_file(args)
        else:
            raise Exception("Could not find " + args.file.name)

    create_recommendations_playlist(args.lastfm_user,
                                    args.spotify_user,
                                    args.recommendation_period,
                                    args.max_recommendations_per_top_track,
                                    args.playlist_size)


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
    parser.add_argument('-f', '--file', type=argparse.FileType('r', encoding='UTF-8'))
    group = parser.add_argument_group()
    group.add_argument('-lu', '--lastfm-user', type=str)
    group.add_argument('-su', '--spotify-user', type=str)
    group.add_argument('-lr', '--recommendation-period', type=str)
    group.add_argument('-ms', '--max-recommendations-per-top-track', type=int)
    group.add_argument('-ps', '--playlist-size', type=int)
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
    return args


if __name__ == "__main__":
    _main()
