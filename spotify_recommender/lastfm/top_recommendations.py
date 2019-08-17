import logging
from numpy.random import choice
from pandas import DataFrame
from . import period


class TopRecommendationsFetcher:
    def __init__(self, similar_fetcher, top_fetcher, recent_fetcher):
        self.similar_fetcher = similar_fetcher
        self.top_fetcher = top_fetcher
        self.recent_fetcher = recent_fetcher

    def fetch(self, user, recommendation_period=period.OVERALL, max_similar_tracks_per_top_track=100, size=40):
        """Fetches recommendations for the given user by fetching their top tracks, then getting tracks similar
        to them, and finally filtering out the user's recent tracks"""

        logging.info("Fetching top recommendations for " + user)

        top_tracks = self.top_fetcher.fetch(user=user, a_period=recommendation_period)

        recommendations = []
        for top_track in top_tracks:
            try:
                similar_tracks = self.similar_fetcher.fetch(top_track, max_similar_tracks_per_top_track)
                if similar_tracks:
                    recommendations = recommendations + similar_tracks
            except Exception as e:
                logging.error(f"Error occurred fetching similar tracks: " + str(e))

        logging.debug(f"Before filtering, fetched " + str(len(recommendations)) + " recommendations: " + str(recommendations))

        recent_tracks = self.recent_fetcher.fetch(user=user)

        # TODO This takes surprisingly long
        logging.info("Filtering out recent tracks from recommendations...")
        recommendations = [track for track in recommendations if track not in recent_tracks]

        recommendations = self._get_random_weighted_recommendations(recommendations, size)

        # Filter out duplicates
        recommendations = list(set(recommendations))

        logging.info(f"Fetched " + str(len(recommendations)) + " recommendations: " + str(recommendations))

        return recommendations

    def _get_random_weighted_recommendations(self, recommendations, size):
        ratings = [recommendation.recommendation_rating for recommendation in recommendations]
        ratings_total = sum(ratings)
        logging.debug(f"Ratings total: " + str(ratings_total))
        weights = [recommendation.recommendation_rating / ratings_total for recommendation in recommendations]
        logging.debug(f"Weights: " + str(weights))
        recommendations = choice(recommendations, size=size, p=weights)
        return recommendations
