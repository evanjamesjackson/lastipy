import logging
from .similar_tracks import SimilarTracksFetcher
from .top_tracks import TopTracksFetcher
from . import period


class TopRecommendationsFetcher:
    def __init__(self):
        self.similar_fetcher = SimilarTracksFetcher()
        self.top_fetcher = TopTracksFetcher()

    def fetch(self, user, recommendation_period=period.OVERALL, max_similar_tracks_per_top_track=100):
        top_tracks = self.top_fetcher.fetch(user=user, period=recommendation_period)

        recommendations = []
        for top_track in top_tracks:
            try:
                similar_tracks = self.similar_fetcher.fetch(top_track, max_similar_tracks_per_top_track)
                if similar_tracks:
                    recommendations = recommendations + similar_tracks
            except Exception as error:
                print(error)

        logging.info("Fetched " + str(len(recommendations)) + " recommendations")
