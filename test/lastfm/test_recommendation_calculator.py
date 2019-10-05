import unittest
from src.lastfm.scrobbled_track import ScrobbledTrack
from src.lastfm.recommended_track import RecommendedTrack
from src.lastfm import recommendation_calculator


class RecommendationCalculatorTest(unittest.TestCase):
    def test_rating_with_one_top_track_one_recommendation(self):
        scrobbled_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        recommendations = {
            scrobbled_track: [recommended_track_1]
        }
        recommendation_calculator.calculate(recommendations)
        self.assertEqual(1, recommended_track_1.recommendation_rating)

    def test_rating_with_one_top_track_multiple_recommendations(self):
        scrobbled_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        recommended_track_2 = RecommendedTrack(artist="The Beatles", track_name='Baby You\'re a Rich Man')
        recommended_track_3 = RecommendedTrack(artist="The Beatles", track_name="Blue Jay Way")
        recommendations = {
            scrobbled_track: [recommended_track_1, recommended_track_2, recommended_track_3]
        }
        recommendation_calculator.calculate(recommendations)
        self.assertEqual(1 / 3, recommended_track_1.recommendation_rating)
        self.assertEqual(1 / 3, recommended_track_2.recommendation_rating)
        self.assertEqual(1 / 3, recommended_track_3.recommendation_rating)

    def test_rating_with_multiple_top_tracks_multiple_recommendations(self):
        scrobbled_track_1 = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        recommended_track_2 = RecommendedTrack(artist="The Beatles", track_name='Baby You\'re a Rich Man')
        recommended_track_3 = RecommendedTrack(artist="The Beatles", track_name="Blue Jay Way")
        scrobbled_track_2 = ScrobbledTrack(artist='The Rolling Stones', track_name='Satisfaction', playcount=20)
        recommended_track_4 = RecommendedTrack(artist='The Rolling Stones', track_name='Ruby Tuesday')
        recommended_track_5 = RecommendedTrack(artist="The Beatles", track_name='Get Off Of My Cloud')
        recommendations = {
            scrobbled_track_1: [recommended_track_1, recommended_track_2, recommended_track_3],
            scrobbled_track_2: [recommended_track_4, recommended_track_5]
        }
        recommendation_calculator.calculate(recommendations)
        self.assertEqual(1 / 7, recommended_track_1.recommendation_rating)
        self.assertEqual(1 / 7, recommended_track_2.recommendation_rating)
        self.assertEqual(1 / 7, recommended_track_3.recommendation_rating)
        self.assertEqual(2 / 7, recommended_track_4.recommendation_rating)
        self.assertEqual(2 / 7, recommended_track_5.recommendation_rating)
