import unittest
from src.lastfm.library.scrobbled_track import ScrobbledTrack
from src.lastfm.recommendations.recommended_track import RecommendedTrack
from src.lastfm.recommendations.rating_calculator import RatingCalculator
from unittest.mock import MagicMock
from src.lastfm.library.recent_artists import RecentArtistsFetcher
from src.lastfm.library.scrobbled_artist import ScrobbledArtist


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
        self.assertEqual(10, recommendations[0].recommendation_rating)

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
        self.assertEqual(10, recommendations[0].recommendation_rating)
        self.assertEqual(10, recommendations[1].recommendation_rating)
        self.assertEqual(10, recommendations[2].recommendation_rating)

    def test_rating_with_multiple_top_tracks_multiple_recommendations(self):
        recent_artist_fetcher = RecentArtistsFetcher()
        recent_artist_fetcher.fetch = MagicMock(return_value=[])
        scrobbled_track_1 = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        recommended_track_2 = RecommendedTrack(artist="The Beatles", track_name='Baby You\'re a Rich Man')
        recommended_track_3 = RecommendedTrack(artist="The Beatles", track_name="Blue Jay Way")
        scrobbled_track_2 = ScrobbledTrack(artist='The Rolling Stones', track_name='Satisfaction', playcount=20)
        recommended_track_4 = RecommendedTrack(artist='The Rolling Stones', track_name='Ruby Tuesday')
        recommended_track_5 = RecommendedTrack(artist="The Beatles", track_name='Get Off Of My Cloud')
        top_tracks_to_recommendations = {
            scrobbled_track_1: [recommended_track_1, recommended_track_2, recommended_track_3],
            scrobbled_track_2: [recommended_track_4, recommended_track_5]
        }
        recommendations = RatingCalculator(recent_artist_fetcher).calculate('test', top_tracks_to_recommendations)
        self.assertEqual(10, recommendations[0].recommendation_rating)
        self.assertEqual(10, recommendations[1].recommendation_rating)
        self.assertEqual(10, recommendations[2].recommendation_rating)
        self.assertEqual(20, recommendations[3].recommendation_rating)
        self.assertEqual(20, recommendations[4].recommendation_rating)

    def test_rating_is_reduced_based_on_artist_playcount(self):
        recent_artist_fetcher = RecentArtistsFetcher()
        recent_artist_fetcher.fetch = MagicMock(return_value=[ScrobbledArtist(artist_name='The Beatles', playcount=9)])
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
        recent_artist_fetcher.fetch = MagicMock(return_value=[ScrobbledArtist(artist_name='The Beatles', playcount=9),
                                                              ScrobbledArtist(artist_name='The Rolling Stones', playcount=19)])
        scrobbled_track_1 = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=5)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        scrobbled_track_2 = ScrobbledTrack(artist='The Rolling Stones', track_name='Satisfaction', playcount=10)
        recommended_track_2 = RecommendedTrack(artist='The Kinks', track_name='You Really Got Me')
        recommended_track_3 = RecommendedTrack(artist='The Rolling Stones', track_name='Ruby Tuesday')
        top_tracks_to_recommendations = {
            scrobbled_track_1: [recommended_track_1],
            scrobbled_track_2: [recommended_track_2, recommended_track_3]
        }
        recommendations = RatingCalculator(recent_artist_fetcher).calculate('test', top_tracks_to_recommendations)
        self.assertEqual(0.5, recommendations[0].recommendation_rating)
        self.assertEqual(10, recommendations[1].recommendation_rating)
        self.assertEqual(0.5, recommendations[2].recommendation_rating)

    def test_recommendations_where_artist_has_one_playcount_should_get_rating_halved(self):
        recent_artist_fetcher = RecentArtistsFetcher()
        recent_artist_fetcher.fetch = MagicMock(return_value=[ScrobbledArtist(artist_name='The Beatles', playcount=1)])
        scrobbled_track = ScrobbledTrack(artist='The Beatles', track_name='Penny Lane', playcount=10)
        recommended_track_1 = RecommendedTrack(artist='The Beatles', track_name='Strawberry Fields Forever')
        top_tracks_to_recommendations = {
            scrobbled_track: [recommended_track_1]
        }
        recommendations = RatingCalculator(recent_artist_fetcher).calculate('test', top_tracks_to_recommendations)
        self.assertEqual(5, recommendations[0].recommendation_rating)
