import unittest
from src.lastfm.scrobbled_track import ScrobbledTrack
from src.lastfm.recommended_track import RecommendedTrack
from src.lastfm import recommendation_calculator


class RecommendationCalculatorTest(unittest.TestCase):
    def test_rating_is_based_on_top_track_playcount(self):
        scrobbled_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        recommendations = {
            scrobbled_track: [recommended_track_1]
        }
        recommendation_calculator.calculate(recommendations)
        self.assertEqual(10, recommended_track_1.recommendation_rating)
