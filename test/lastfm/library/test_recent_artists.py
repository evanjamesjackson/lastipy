import unittest
from unittest.mock import patch
from lastipy.lastfm.library import recent_artists
from lastipy.lastfm.library.scrobbled_artist import ScrobbledArtist
from unittest.mock import Mock


class RecentArtistsTest(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_single_page_no_errors(self, mock_requests_get):
        expected_artists = [
            ScrobbledArtist(artist_name='Bee Gees', playcount=5),
            ScrobbledArtist(artist_name='The Beatles', playcount=10)
        ]

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            'artists': {
                'artist': [
                    {
                        'name': 'Bee Gees',
                        'playcount': '5'
                    },
                    {
                        'name': 'The Beatles',
                        'playcount': '10'
                    }
                ],
                '@attr': {
                    'totalPages': '1'
                }
            }
        }
        mock_requests_get.side_effect = [mock_response]

        dummy_user = 'testUser'
        dummy_api_key = '123456789'

        fetched_artists = recent_artists.fetch_recent_artists(user=dummy_user, api_key=dummy_api_key)

        self.assertCountEqual(fetched_artists, expected_artists)        