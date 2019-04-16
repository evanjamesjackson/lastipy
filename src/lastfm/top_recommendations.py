import logging
from .similar_tracks import SimilarTracksFetcher
from .top_tracks import TopTracksFetcher
from . import period


class TopRecommendationsFetcher:
    def __init__(self, similar_fetcher, top_fetcher, recent_fetcher):
        self.similar_fetcher = similar_fetcher
        self.top_fetcher = top_fetcher
        self.recent_fetcher = recent_fetcher

    def fetch(self, user, recommendation_period=period.OVERALL, max_similar_tracks_per_top_track=100):
        logging.info("Fetching top recommendations for " + user)

        top_tracks = self.top_fetcher.fetch(user=user, a_period=recommendation_period)

        recommendations = []
        for top_track in top_tracks:
            similar_tracks = self.similar_fetcher.fetch(top_track, max_similar_tracks_per_top_track)
            if similar_tracks:
                recommendations = recommendations + similar_tracks

        logging.debug(f"Before filtering, fetched " + str(len(recommendations)) + " recommendations: " + str(recommendations))

        logging.info("Filtering out recent tracks from recommendations")
        recent_tracks = self.recent_fetcher.fetch(user=user)
        recommendations = [track for track in recommendations if track not in recent_tracks]

        logging.info(f"Fetched " + str(len(recommendations)) + " recommendations: " + str(recommendations))

        return recommendations
