import logging, os
from spotify_recommender import definitions
from spotify_recommender.lastfm import period
from spotify_recommender.lastfm.top_tracks import TopTracksFetcher
from spotify_recommender.lastfm.similar_tracks import SimilarTracksFetcher
from spotify_recommender.lastfm.top_recommendations import TopRecommendationsFetcher
from spotify_recommender.lastfm.recent_tracks import RecentTracksFetcher
from spotify_recommender.spotify import library, playlist, search
from random import shuffle


def main():
    # TODO put these somewhere. Or maybe command-line arguments?
    lastfm_user = 'sonofjack3'
    lastfm_recommendation_period = period.ONE_MONTH
    max_similar_tracks_per_top_track = 50
    spotify_user = 'sonofjack3'
    playlist_size = 40
    playlist_name = "LastFM"

    log_file = os.path.join(definitions.ROOT_DIR, ".log")
    logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler(filename=log_file, mode='w', encoding='utf-8'), logging.StreamHandler()])

    recommendations_fetcher = TopRecommendationsFetcher(similar_fetcher=SimilarTracksFetcher(),
                                                        top_fetcher=TopTracksFetcher(),
                                                        recent_fetcher=RecentTracksFetcher())
    recommendations = recommendations_fetcher.fetch(user=lastfm_user,
                                                    recommendation_period=lastfm_recommendation_period,
                                                    max_similar_tracks_per_top_track=max_similar_tracks_per_top_track)

    shuffle(recommendations)

    track_ids = []
    for track in recommendations[:playlist_size]:
        search_results = search.search(username=spotify_user, query=track.artist + " " + track.track_name)
        if search_results['tracks']['items']:
            track_ids.append(search_results['tracks']['items'][0]['id'])

    saved_tracks = library.get_saved_tracks('sonofjack3')
    playlist_tracks = library.get_tracks_in_playlists(spotify_user)

    track_ids = [track_id for track_id in track_ids if track_id not in saved_tracks and track_id not in playlist_tracks]

    playlist.add_to_playlist(spotify_user, playlist_name, track_ids)


if __name__ == "__main__":
    main()
