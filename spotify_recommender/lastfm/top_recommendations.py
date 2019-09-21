import logging
from spotify_recommender.lastfm import period
from spotify_recommender.track import Track
import numpy


class TopRecommendationsFetcher:
    def __init__(self, similar_fetcher, top_fetcher, recent_fetcher, recent_artists_fetcher):
        self.similar_fetcher = similar_fetcher
        self.top_fetcher = top_fetcher
        self.recent_fetcher = recent_fetcher
        self.recent_artists_fetcher = recent_artists_fetcher

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

        recommendations = self._filter_out_recent_tracks(recent_tracks, recommendations)

        recommendations = self._filter_out_blacklisted_artists(blacklisted_artists, recommendations)

        if prefer_unheard_artists:
            self._adjust_recommendation_rating_by_artist(recommendations, user)

        # Filter out duplicates
        # TODO maybe duplicates should mean a greater chance of getting that recommendation in the playlist?
        recommendations = list(set(recommendations))

        logging.info(f"Fetched " + str(len(recommendations)) + " recommendations: " + str(recommendations))

        return recommendations

    def _adjust_recommendation_rating_by_artist(self, recommendations, user):
        logging.info("Adjusting recommendations so that tracks by frequently-played artists get lower ratings...")
        recent_artists = self.recent_artists_fetcher.fetch(user)
        for recommendation in recommendations:
            for artist in recent_artists:
                if recommendation.artist == artist.artist_name:
                    recommendation.recommendation_rating = (1 / artist.playcount) * recommendation.recommendation_rating

    def _filter_out_blacklisted_artists(self, blacklisted_artists, recommendations):
        logging.info("Filtering out blacklisted artists (" + str(blacklisted_artists) + ")...")
        recommendations = [recommendation for recommendation in recommendations
                           if not any(recommendation.artist == blacklisted_artist
                                      for blacklisted_artist in blacklisted_artists)]
        return recommendations

    def _filter_out_recent_tracks(self, recent_tracks, recommendations):
        logging.info("Filtering out recent tracks from recommendations...")
        recommendations = [recommendation for recommendation in recommendations
                           if not any(Track.are_equivalent(recommendation, recent_track)
                                      for recent_track in recent_tracks)]
        return recommendations
