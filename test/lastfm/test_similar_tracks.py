import unittest
from src.lastfm.similar_tracks import SimilarTracksFetcher
from src.lastfm.track import Track
from unittest.mock import patch

class SimilarTracksFetcherTest(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_top_track_success(self, mock_get):
        expected_tracks = [
            Track(track_name="Stayin' Alive", artist="Bee Gees"),
            Track(track_name="You Should Be Dancing", artist="Bee Gees")
        ]
        track_to_send = Track(track_name="Night Fever", artist="Bee Gees")

        json_tracks = []
        for expected_track in expected_tracks:
            json_track = {
                'name': expected_track.track_name,
                'artist': {
                    'name': expected_track.artist
                }
            }
            json_tracks.append(json_track)
            

        json_response = {
            'similartracks': {
                'track': json_tracks
            }
        }
        
        mock_get.return_value.json.return_value = json_response

        fetcher = SimilarTracksFetcher()
        self.assertCountEqual(expected_tracks, fetcher.fetch(track_to_send, 2))