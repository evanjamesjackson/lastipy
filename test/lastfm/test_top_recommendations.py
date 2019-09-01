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
        recent_track_1 = ScrobbledTrack(track_name="SWALBR", artist="Cream", playcount=1)
        recent_track_2 = ScrobbledTrack(track_name="Badge", artist="Cream", playcount=5)
        recent_track_3 = ScrobbledTrack(track_name="Layla", artist="Derek & the Dominos", playcount=8)
        recent_fetcher.fetch = MagicMock(return_value=[recent_track_1, recent_track_2, recent_track_3])

        top_fetcher = TopTracksFetcher()
        top_fetcher.fetch = MagicMock(return_value=[recent_track_3])

        similar_fetcher = SimilarTracksFetcher()
        new_recommendation = RecommendedTrack(track_name="Key to the Highway", artist="Derek & the Dominos", recommendation_rating=8)
        already_scrobbled_recommendation_1 = RecommendedTrack(track_name="Badge", artist="Cream", recommendation_rating=8)
        already_scrobbled_recommendation_2 = RecommendedTrack(track_name="SWALBR", artist="Cream", recommendation_rating=8)
        similar_fetcher.fetch = MagicMock(return_value=[new_recommendation,
                                                        already_scrobbled_recommendation_1,
                                                        already_scrobbled_recommendation_2])

        recommendations = TopRecommendationsFetcher(similar_fetcher=similar_fetcher,
                                                    top_fetcher=top_fetcher,
                                                    recent_fetcher=recent_fetcher).fetch(user="meeee")

        self.assertCountEqual(recommendations, [new_recommendation])

    def test_blacklisted_artists_are_filtered(self):
        recent_fetcher = RecentTracksFetcher()
        recent_fetcher.fetch = MagicMock(return_value=[])
        top_fetcher = TopTracksFetcher()
        top_fetcher.fetch = MagicMock(return_value=[ScrobbledTrack(track_name='Here Comes the Sun', artist='The Beatles', playcount=5)])

        similar_fetcher = SimilarTracksFetcher()
        recommendation_1 = RecommendedTrack(track_name="Badge", artist="Cream", recommendation_rating=1)
        recommendation_2 = RecommendedTrack(track_name="Penny Lane", artist="The Beatles", recommendation_rating=1)
        similar_fetcher.fetch = MagicMock(return_value=[recommendation_1, recommendation_2])

        recommendations = TopRecommendationsFetcher(similar_fetcher=similar_fetcher,
                                                    top_fetcher=top_fetcher,
                                                    recent_fetcher=recent_fetcher).fetch(
                                                        user="meeee",
                                                        blacklisted_artists=['The Beatles'])

        self.assertCountEqual(recommendations, [recommendation_1])
