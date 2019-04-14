from .similar_tracks import SimilarTracksFetcher
from .top_tracks import TopTracksFetcher
from . import period

class TopRecommendationsFetcher:
    def __init__(self):
        self.similar_fetcher = SimilarTracksFetcher()
        self.top_fetcher = TopTracksFetcher()

    def fetch(self, user, recommendation_period=period.OVERALL, max_similar_tracks_per_top_track=100):
        print("Fetching top tracks for user " + user + " over period " + recommendation_period)
        fetcher = TopTracksFetcher()
        top_tracks = fetcher.fetch(user=user, period=recommendation_period)
        print(f'Fetched {len(top_tracks)} top tracks')
        print("Top tracks: " + str(top_tracks))

        similar_tracks_fetcher = SimilarTracksFetcher()
        all_similar_tracks = []
        for top_track in top_tracks:
            try:
                print("Fetching tracks similar to " + str(top_track))
                similar_tracks = similar_tracks_fetcher.fetch(top_track,
                                                              max_similar_tracks_per_top_track)
                print("Fetched: " + str(similar_tracks))
                if similar_tracks:
                    all_similar_tracks = all_similar_tracks + similar_tracks
            except Exception as error:
                print(error)
        print(f'Fetched {len(all_similar_tracks)} similar tracks in total')
