import unittest
from unittest.mock import MagicMock
from spotify_recommender.lastfm.similar_tracks import SimilarTracksFetcher
from spotify_recommender.lastfm.top_tracks import TopTracksFetcher
from spotify_recommender.lastfm.recent_tracks import RecentTracksFetcher
from spotify_recommender.lastfm.top_recommendations import TopRecommendationsFetcher
from spotify_recommender.lastfm.recommended_track import RecommendedTrack
from spotify_recommender.lastfm.scrobbled_track import ScrobbledTrack


class TopRecommendationsFetcherTest(unittest.TestCase):
    def test_recent_tracks_are_filtered(self):
        recent_fetcher = RecentTracksFetcher()
        recent_track = ScrobbledTrack(track_name="While My Guitar Gently Weeps", artist="The Beatles", playcount=1)
        recent_fetcher.fetch = MagicMock(return_value=[recent_track])

        top_fetcher = TopTracksFetcher()
        top_fetcher.fetch = MagicMock(return_value=[ScrobbledTrack(track_name="Badge", artist="Cream", playcount=5)])

        similar_fetcher = SimilarTracksFetcher()
        expected_recommendation = RecommendedTrack(track_name="White Room", artist="Cream", recommendation_rating=5)
        similar_fetcher.fetch = MagicMock(return_value=[recent_track,
                                                        expected_recommendation])

        recommendations = TopRecommendationsFetcher(similar_fetcher=similar_fetcher, top_fetcher=top_fetcher, recent_fetcher=recent_fetcher).fetch(user="meeee")

        self.assertCountEqual(recommendations, [expected_recommendation])

    def test_weighed_randomizer(self):
        fetcher = TopRecommendationsFetcher(similar_fetcher=SimilarTracksFetcher(), top_fetcher=TopTracksFetcher(), recent_fetcher=RecentTracksFetcher())
        recommended_track_1 = RecommendedTrack(track_name="Penny Lane", artist="The Beatles", recommendation_rating=5)
        recommended_track_2 = RecommendedTrack(track_name="Strawberry Fields Forever", artist="The Beatles", recommendation_rating=10)
        recommended_track_3 = RecommendedTrack(track_name="Hey Bulldog", artist="The Beatles", recommendation_rating=6)
        recommendations = [recommended_track_1, recommended_track_2, recommended_track_3]
        recommendations = fetcher._get_random_weighted_recommendations(recommendations=recommendations, size=3)
        self.assertEqual(3, len(recommendations))
