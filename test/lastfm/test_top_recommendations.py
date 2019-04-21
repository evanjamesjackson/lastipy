import unittest
from unittest.mock import MagicMock
from spotify_recommender.lastfm.similar_tracks import SimilarTracksFetcher
from spotify_recommender.lastfm.top_tracks import TopTracksFetcher
from spotify_recommender.lastfm.recent_tracks import RecentTracksFetcher
from spotify_recommender.lastfm.top_recommendations import TopRecommendationsFetcher
from spotify_recommender.track import Track


class TopRecommendationsFetcherTest(unittest.TestCase):
    def test_recent_tracks_are_filtered(self):
        recent_fetcher = RecentTracksFetcher()
        recent_track = Track(track_name="While My Guitar Gently Weeps", artist="The Beatles")
        recent_fetcher.fetch = MagicMock(return_value=[recent_track])

        top_fetcher = TopTracksFetcher()
        top_fetcher.fetch = MagicMock(return_value=[Track(track_name="Badge", artist="Cream")])

        similar_fetcher = SimilarTracksFetcher()
        expected_recommendation = Track(track_name="White Room", artist="Cream")
        similar_fetcher.fetch = MagicMock(return_value=[recent_track,
                                                        expected_recommendation])

        recommendations = TopRecommendationsFetcher(similar_fetcher=similar_fetcher, top_fetcher=top_fetcher, recent_fetcher=recent_fetcher).fetch(user="meeee")

        self.assertCountEqual(recommendations, [expected_recommendation])
