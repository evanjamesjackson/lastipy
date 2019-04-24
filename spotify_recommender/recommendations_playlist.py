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
from random import shuffle
from configparser import ConfigParser
import os
from spotify_recommender import definitions

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

    shuffle(recommendations)

    track_ids = []
    for track in recommendations[:playlist_size]:
        track_ids = track_ids + search.search_for_tracks(
            username=spotify_user,
            query=track.artist + " " + track.track_name)

    logging.info("Filtering out library and playlist tracks")
    saved_tracks = library.get_saved_tracks(spotify_user)
    playlist_tracks = library.get_tracks_in_playlists(spotify_user)
    track_ids = [track_id for track_id in track_ids if track_id not in saved_tracks and track_id not in playlist_tracks]

    playlist.add_to_playlist(spotify_user, PLAYLIST_NAME, track_ids)


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

    logging.basicConfig(level=logging.DEBUG,
                        format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.handlers.RotatingFileHandler(
                            filename=os.path.join(logs_directory, 'spotify_recommender.log'),
                            maxBytes=7 * 1024 * 1024,  # 7 MB
                            backupCount=10,
                            encoding='utf-8'),
                            logging.StreamHandler()])


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
