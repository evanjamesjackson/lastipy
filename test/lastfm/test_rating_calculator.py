import unittest
from src.lastfm.scrobbled_track import ScrobbledTrack
from src.lastfm.recommended_track import RecommendedTrack
from src.lastfm.rating_calculator import RatingCalculator
from unittest.mock import MagicMock
from src.lastfm.recent_artists import RecentArtistsFetcher
from src.lastfm.scrobbled_artist import ScrobbledArtist


class RatingCalculatorTest(unittest.TestCase):
    def test_rating_with_one_top_track_one_recommendation(self):
        recent_artist_fetcher = RecentArtistsFetcher()
        recent_artist_fetcher.fetch = MagicMock(return_value=[])
        scrobbled_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        top_tracks_to_recommendations = {
            scrobbled_track: [recommended_track_1]
        }
        recommendations = RatingCalculator(recent_artist_fetcher).calculate('test', top_tracks_to_recommendations)
        self.assertEqual(1, recommendations[0].recommendation_rating)

    def test_rating_with_one_top_track_multiple_recommendations(self):
        recent_artist_fetcher = RecentArtistsFetcher()
        recent_artist_fetcher.fetch = MagicMock(return_value=[])
        scrobbled_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        recommended_track_2 = RecommendedTrack(artist="The Beatles", track_name='Baby You\'re a Rich Man')
        recommended_track_3 = RecommendedTrack(artist="The Beatles", track_name="Blue Jay Way")
        top_tracks_to_recommendations = {
            scrobbled_track: [recommended_track_1, recommended_track_2, recommended_track_3]
        }
        recommendations = RatingCalculator(recent_artist_fetcher).calculate('test', top_tracks_to_recommendations)
        self.assertEqual(1 / 3, recommendations[0].recommendation_rating)
        self.assertEqual(1 / 3, recommendations[1].recommendation_rating)
        self.assertEqual(1 / 3, recommendations[2].recommendation_rating)

    def test_rating_with_multiple_top_tracks_multiple_recommendations(self):
        recent_artist_fetcher = RecentArtistsFetcher()
        recent_artist_fetcher.fetch = MagicMock(return_value=[])
        scrobbled_track_1 = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        recommended_track_2 = RecommendedTrack(artist="The Beatles", track_name='Baby You\'re a Rich Man')
        recommended_track_3 = RecommendedTrack(artist="The Beatles", track_name="Blue Jay Way")
        scrobbled_track_2 = ScrobbledTrack(artist='The Rolling Stones', track_name='Satisfaction', playcount=10)
        recommended_track_4 = RecommendedTrack(artist='The Rolling Stones', track_name='Ruby Tuesday')
        recommended_track_5 = RecommendedTrack(artist="The Beatles", track_name='Get Off Of My Cloud')
        top_tracks_to_recommendations = {
            scrobbled_track_1: [recommended_track_1, recommended_track_2, recommended_track_3],
            scrobbled_track_2: [recommended_track_4, recommended_track_5]
        }
        recommendations = RatingCalculator(recent_artist_fetcher).calculate('test', top_tracks_to_recommendations)
        self.assertEqual(1 / 5, recommendations[0].recommendation_rating)
        self.assertEqual(1 / 5, recommendations[1].recommendation_rating)
        self.assertEqual(1 / 5, recommendations[2].recommendation_rating)
        self.assertEqual(1 / 5, recommendations[3].recommendation_rating)
        self.assertEqual(1 / 5, recommendations[4].recommendation_rating)

    def test_rating_is_reduced_based_on_artist_playcount(self):
        recent_artist_fetcher = RecentArtistsFetcher()
        recent_artist_fetcher.fetch = MagicMock(return_value=[ScrobbledArtist(artist_name='The Beatles', playcount=10)])
        scrobbled_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=5)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        recommended_track_2 = RecommendedTrack(artist='The Beatles', track_name='Blue Jay Way')
        top_tracks_to_recommendations = {
            scrobbled_track: [recommended_track_1, recommended_track_2]
        }
        recommendations = RatingCalculator(recent_artist_fetcher).calculate('test', top_tracks_to_recommendations)
        self.assertEqual(0.5, recommendations[0].recommendation_rating)
        self.assertEqual(0.5, recommendations[1].recommendation_rating)

    def test_multiple_recommendations_and_multiple_recent_artists(self):
        recent_artist_fetcher = RecentArtistsFetcher()
        recent_artist_fetcher.fetch = MagicMock(return_value=[ScrobbledArtist(artist_name='The Beatles', playcount=10),
                                                              ScrobbledArtist(artist_name='The Rolling Stones', playcount=18)])
        scrobbled_track_1 = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=5)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        scrobbled_track_2 = ScrobbledTrack(artist='The Rolling Stones', track_name='Satisfaction', playcount=9)
        recommended_track_2 = RecommendedTrack(artist='The Kinks', track_name='You Really Got Me')
        recommended_track_3 = RecommendedTrack(artist='The Rolling Stones', track_name='Ruby Tuesday')
        top_tracks_to_recommendations = {
            scrobbled_track_1: [recommended_track_1],
            scrobbled_track_2: [recommended_track_2, recommended_track_3]
        }
        recommendations = RatingCalculator(recent_artist_fetcher).calculate('test', top_tracks_to_recommendations)
        # Total = 0.5 + 9 + 0.5 = 10
        self.assertEqual(0.05, recommendations[0].recommendation_rating)
        self.assertEqual(0.9, recommendations[1].recommendation_rating)
        self.assertEqual(0.05, recommendations[2].recommendation_rating)
