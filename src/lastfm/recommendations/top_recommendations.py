import logging
from src.lastfm.library import period
from src.track import Track


class TopRecommendationsFetcher:
    def __init__(self, similar_fetcher, top_fetcher, recent_fetcher, rating_calculator):
        self.similar_fetcher = similar_fetcher
        self.top_fetcher = top_fetcher
        self.recent_fetcher = recent_fetcher
        self.rating_calculator = rating_calculator

    def fetch(self,
              user,
              recommendation_period=period.OVERALL,
              max_similar_tracks_per_top_track=100,
              blacklisted_artists=[],
              prefer_unheard_artists=True):
        """Fetches recommendations for the given user by fetching their top tracks, then getting tracks similar
        to them, and finally filtering out the user's recent tracks"""

        logging.info("Fetching top recommendations for " + user)

        top_tracks = self.top_fetcher.fetch(user=user, a_period=recommendation_period)

        top_tracks_to_recommendations = {}
        all_recommendations = []
        for top_track in top_tracks:
            try:
                current_recommendations = self.similar_fetcher.fetch(top_track, max_similar_tracks_per_top_track)
                if current_recommendations:
                    all_recommendations = all_recommendations + current_recommendations
                    top_tracks_to_recommendations[top_track] = current_recommendations
            except Exception as e:
                logging.error(f"Error occurred fetching similar tracks: " + str(e))

        all_recommendations = self.rating_calculator.calculate(user=user,
                                                               prefer_unheard_artists=prefer_unheard_artists,
                                                               top_tracks_to_recommendations=top_tracks_to_recommendations)

        logging.debug(f"Before filtering, fetched " + str(len(all_recommendations)) + " recommendations: " + str(all_recommendations))

        all_recommendations = self._filter_out_recent_tracks(user, all_recommendations)

        all_recommendations = self._filter_out_blacklisted_artists(blacklisted_artists, all_recommendations)

        # Filter out duplicates
        # TODO maybe duplicates should mean a greater chance of getting that recommendation in the playlist?
        all_recommendations = list(set(all_recommendations))

        logging.info(f"Fetched " + str(len(all_recommendations)) + " recommendations: " + str(all_recommendations))

        return all_recommendations

    def _filter_out_blacklisted_artists(self, blacklisted_artists, recommendations):
        logging.info("Filtering out blacklisted artists (" + str(blacklisted_artists) + ")...")
        recommendations = [recommendation for recommendation in recommendations
                           if not any(recommendation.artist == blacklisted_artist
                                      for blacklisted_artist in blacklisted_artists)]
        return recommendations

    def _filter_out_recent_tracks(self, user, recommendations):
        recent_tracks = self.recent_fetcher.fetch(user=user)
        logging.info("Filtering out recent tracks from recommendations...")
        recommendations = [recommendation for recommendation in recommendations
                           if not any(Track.are_equivalent(recommendation, recent_track)
                                      for recent_track in recent_tracks)]
        return recommendations
