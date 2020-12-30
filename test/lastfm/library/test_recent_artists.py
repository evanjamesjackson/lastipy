import unittest
from unittest.mock import patch
from lastipy.lastfm.library import recent_artists
from lastipy.lastfm.library.scrobbled_artist import ScrobbledArtist
from unittest.mock import Mock


class RecentArtistsTest(unittest.TestCase):

    dummy_user = 'dummyUser'
    dummy_api_key = '123456789'

    @patch('requests.get')
    def test_fetch_single_page(self, mock_requests_get):
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

        fetched_artists = recent_artists.fetch_recent_artists(user=self.dummy_user, api_key=self.dummy_api_key)

        self.assertCountEqual(fetched_artists, expected_artists)

    @patch('requests.get')
    def test_fetch_multiple_pages(self, mock_requests_get):
        expected_artists = [
            ScrobbledArtist(artist_name='Bee Gees', playcount=5),
            ScrobbledArtist(artist_name='The Beatles', playcount=10),
            ScrobbledArtist(artist_name='Cream', playcount=15)
        ]

        mock_responses = [Mock(), Mock(), Mock()]
        mock_responses[0].ok = True
        mock_responses[0].json.return_value = self._build_artist_json_response('Bee Gees', '5', '3')
        mock_responses[1].ok = True
        mock_responses[1].json.return_value = self._build_artist_json_response('The Beatles', '10', '3')
        mock_responses[2].ok = True
        mock_responses[2].json.return_value = self._build_artist_json_response('Cream', '15', '3')
        mock_requests_get.side_effect = mock_responses

        fetched_artists = recent_artists.fetch_recent_artists(user=self.dummy_user, api_key=self.dummy_api_key)

        self.assertCountEqual(fetched_artists, expected_artists)

    def _build_artist_json_response(self, artist_name, playcount, total_pages):
        return { 'artists': { 'artist': [ { 'name': artist_name, 'playcount': playcount } ], '@attr': { 'totalPages': total_pages } } }
