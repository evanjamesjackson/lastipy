import unittest
from src.lastfm.library.top_track import TopTrack
from src.lastfm.recommendations.recommended_track import RecommendedTrack
from unittest.mock import patch
from src.lastfm.recommendations.similar_tracks import fetch_similar_tracks


class SimilarTracksFetcherTest(unittest.TestCase):
    
    @patch('requests.get')
    @patch('src.parse_keys.get_lastfm_key')
    # The order of the mock parameters is the reverse of the above patched functions. Yes, really.
    def test_track_has_multiple_similar_tracks(self, mock_parse_keys, mock_requests_get):
        playcount = 5
        track_to_check = TopTrack(track_name="Night Fever", artist="Bee Gees", playcount=playcount)
        expected_similar_tracks = [
            RecommendedTrack(track_name="Stayin' Alive", artist="Bee Gees", recommendation_rating=playcount),
            RecommendedTrack(track_name="You Should Be Dancing", artist="Bee Gees", recommendation_rating=playcount)
        ]

        json_tracks = []
        for track in expected_similar_tracks:
            json_track = {
                'name': track.track_name,
                'artist': {
                    'name': track.artist
                },
                'match': track.recommendation_rating
            }
            json_tracks.append(json_track)

        json_response = {
            'similartracks': {
                'track': json_tracks
            }
        }
        
        mock_requests_get.return_value.json.return_value = json_response
        mock_parse_keys.return_value = ''

        fetched_tracks = fetch_similar_tracks(track_to_check, 2)
        self.assertCountEqual(expected_similar_tracks, fetched_tracks)
        for track in fetched_tracks:
            self.assertEqual(playcount, track.recommendation_rating)