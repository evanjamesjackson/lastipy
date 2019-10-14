import unittest
from unittest.mock import MagicMock
from src.lastfm.recommendations.similar_tracks import SimilarTracksFetcher
from src.lastfm.library.top_tracks import TopTracksFetcher
from src.lastfm.library.recent_tracks import RecentTracksFetcher
from src.lastfm.recommendations.recommendations import RecommendationsFetcher
from src.lastfm.recommendations.recommended_track import RecommendedTrack
from src.lastfm.library.scrobbled_track import ScrobbledTrack


class RecommendationsFetcherTest(unittest.TestCase):
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
        recommendations = [new_recommendation, already_scrobbled_recommendation_1, already_scrobbled_recommendation_2]
        similar_fetcher.fetch = MagicMock(return_value=recommendations)

        rating_calculator = MagicMock()
        rating_calculator.calculate = MagicMock(return_value=recommendations)

        recommendations = RecommendationsFetcher(similar_fetcher=similar_fetcher,
                                                 top_fetcher=top_fetcher,
                                                 recent_fetcher=recent_fetcher,
                                                 rating_calculator=rating_calculator).fetch(user="meeee")

        self.assertCountEqual(recommendations, [new_recommendation])

    def test_blacklisted_artists_are_filtered(self):
        recent_fetcher = RecentTracksFetcher()
        recent_fetcher.fetch = MagicMock(return_value=[])
        top_fetcher = TopTracksFetcher()
        top_fetcher.fetch = MagicMock(return_value=[ScrobbledTrack(track_name='Here Comes the Sun', artist='The Beatles', playcount=5)])

        similar_fetcher = SimilarTracksFetcher()
        recommendation_1 = RecommendedTrack(track_name="Badge", artist="Cream", recommendation_rating=1)
        recommendation_2 = RecommendedTrack(track_name="Penny Lane", artist="The Beatles", recommendation_rating=1)
        recommendations = [recommendation_1, recommendation_2]
        similar_fetcher.fetch = MagicMock(return_value=recommendations)

        rating_calculator = MagicMock()
        rating_calculator.calculate = MagicMock(return_value=recommendations)

        recommendations = RecommendationsFetcher(similar_fetcher=similar_fetcher,
                                                 top_fetcher=top_fetcher,
                                                 recent_fetcher=recent_fetcher,
                                                 rating_calculator=rating_calculator).fetch(
                                                        user="meeee",
                                                        blacklisted_artists=['The Beatles'])

        self.assertCountEqual(recommendations, [recommendation_1])