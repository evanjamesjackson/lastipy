import definitions, logging, os
from src.lastfm import period
from src.lastfm.top_tracks import TopTracksFetcher
from src.lastfm.similar_tracks import SimilarTracksFetcher
from src.lastfm.top_recommendations import TopRecommendationsFetcher
from src.lastfm.recent_tracks import RecentTracksFetcher
from src.spotify.playlist import *
from src.spotify.search import *
from random import shuffle


def main():
    log_file = os.path.join(definitions.ROOT_DIR, ".log")
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler(filename=log_file, mode='w', encoding='utf-8'), logging.StreamHandler()])

    lastfm_user = 'sonofjack3'
    recommendations_fetcher = TopRecommendationsFetcher(similar_fetcher=SimilarTracksFetcher(),
                                                        top_fetcher=TopTracksFetcher(),
                                                        recent_fetcher=RecentTracksFetcher())
    recommendations = recommendations_fetcher.fetch(user=lastfm_user,
                                                    recommendation_period=period.SEVEN_DAYS,
                                                    max_similar_tracks_per_top_track=50)

    shuffle(recommendations)

    # TODO filter out tracks already in Spotify playlists and library

    spotify_user = 'sonofjack3'
    playlist_size = 30
    playlist_name = "LastFM"

    track_ids = []
    for track in recommendations[:playlist_size]:
        search_results = search(username=spotify_user, query=track.artist + " " + track.track_name)
        if search_results['tracks']['items']:
            track_ids.append(search_results['tracks']['items'][0]['id'])

    add_to_playlist(spotify_user, playlist_name, track_ids)

if __name__ == "__main__":
    main()
