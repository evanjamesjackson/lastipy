import unittest
from unittest.mock import MagicMock
from spotipy import Spotify
from lastipy.spotify.library import get_saved_tracks
from lastipy.spotify.spotify_track import SpotifyTrack


class GetSavedTracksTest(unittest.TestCase):

    def setUp(self):
        self.mock_spotify = Spotify()
        self.mock_spotify.current_user = MagicMock({'id': 'dummyUser'})

    def test_fetch_single_page(self):
        expected_saved_tracks = [SpotifyTrack(
            track_name='Penny Lane', artist='The Beatles', spotify_id='123456789')
        ]

        self.mock_spotify.current_user_saved_tracks = MagicMock()
        mock_saved_tracks_response = {
            'items': [{
                'track': {
                    'id': '123456789',
                    'name': 'Penny Lane',
                    'artists': [
                        {
                            'name': 'The Beatles'
                        }
                    ]
                }
            }]
        }
        self.mock_spotify.current_user_saved_tracks.side_effect = [
            mock_saved_tracks_response, {'items': []}]

        fetched_saved_tracks = get_saved_tracks(self.mock_spotify)

        self.assertCountEqual(fetched_saved_tracks, expected_saved_tracks)
