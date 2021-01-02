import unittest
from unittest.mock import MagicMock
from spotipy import Spotify
from lastipy.spotify.library import get_saved_tracks


class GetSavedTracksTest(unittest.TestCase):

    def setUp(self):
        self.mock_spotify = Spotify()
        self.mock_spotify.current_user = MagicMock({'id': 'dummyUser'})

    def test_fetch_single_page(self):
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

        get_saved_tracks(self.mock_spotify)
