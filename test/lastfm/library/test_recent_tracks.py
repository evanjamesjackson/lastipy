import unittest
from unittest.mock import patch
from lastipy.lastfm.library import recent_tracks
from unittest.mock import Mock
from requests import HTTPError
from lastipy.track import Track 


class RecentArtistsTest(unittest.TestCase):

    dummy_user = 'dummyUser'
    dummy_api_key = '123456789'

    @patch('requests.get')
    def test_fetch_single_page(self, mock_requests_get):
        expected_tracks = [
            Track(track_name='Strawberry Fields Forever', artist='The Beatles'),
            Track(track_name='Badge', artist='Cream')
        ]

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = {
            'recenttracks': {
                'track': [
                    {
                        'name': 'Strawberry Fields Forever',
                        'artist': {
                            'name': 'The Beatles'  
                        } 
                    },
                    {
                        'name': 'Badge',
                        'artist': {
                            'name': 'Cream'
                        }
                    }
                ],
                '@attr': {
                    'totalPages': '1'
                }
            }
        }
        mock_requests_get.side_effect = [mock_response]

        fetched_tracks = recent_tracks.fetch_recent_tracks(user=self.dummy_user, api_key=self.dummy_api_key)

        self.assertCountEqual(fetched_tracks, expected_tracks)


    @patch('requests.get')
    def test_fetch_multiple_pages(self, mock_requests_get):
        expected_tracks = [
            Track(track_name='Stayin Alive', artist='Bee Gees'),
            Track(track_name='Penny Lane', artist='The Beatles'),
            Track(track_name='Badge', artist='Cream')
        ]

        mock_responses = [Mock(), Mock(), Mock()]
        mock_responses[0].ok = True
        mock_responses[0].json.return_value = self._build_track_json_response('Stayin Alive', 'Bee Gees', '3')
        mock_responses[1].ok = True
        mock_responses[1].json.return_value = self._build_track_json_response('Penny Lane', 'The Beatles', '3')
        mock_responses[2].ok = True
        mock_responses[2].json.return_value = self._build_track_json_response('Badge', 'Cream', '3')
        mock_requests_get.side_effect = mock_responses

        fetched_tracks = recent_tracks.fetch_recent_tracks(user=self.dummy_user, api_key=self.dummy_api_key)

        self.assertCountEqual(fetched_tracks, expected_tracks)


    @patch('requests.get')
    def test_fetch_with_success_after_retries(self, mock_requests_get):
        expected_tracks = [
            Track(track_name='Stayin Alive', artist='Bee Gees'),
            Track(track_name='Penny Lane', artist='The Beatles'),
        ]

        mock_responses = [Mock(), Mock(), Mock()]
        mock_responses[0].ok = True
        mock_responses[0].json.return_value = self._build_track_json_response('Stayin Alive', 'Bee Gees', '2')
        mock_responses[1].ok = False
        mock_responses[1].raise_for_status.side_effect = HTTPError(Mock(status=500), 'Error')
        mock_responses[2].ok = True
        mock_responses[2].json.return_value = self._build_track_json_response('Penny Lane', 'The Beatles', '2')
        mock_requests_get.side_effect = mock_responses

        fetched_tracks = recent_tracks.fetch_recent_tracks(user=self.dummy_user, api_key=self.dummy_api_key)

        self.assertCountEqual(fetched_tracks, expected_tracks)


    @patch('requests.get')
    def test_fetch_fails_after_retries(self, mock_requests_get):
        mock_responses = []
        for _ in range(10):
            mock_response = Mock()
            mock_response.ok = False
            mock_response.raise_for_status.side_effect = HTTPError(Mock(status=500), 'Error')
            mock_responses.append(mock_response)

        # Add another mock response, but the code will exit after the retry limit is reached and this won't actually get fetched
        mock_response = Mock()
        mock_response.ok = False
        mock_response.json.return_value = self._build_track_json_response('Penny Lane', 'The Beatles', '1')

        fetched_tracks = recent_tracks.fetch_recent_tracks(user=self.dummy_user, api_key=self.dummy_api_key)

        self.assertEqual(fetched_tracks, [])


    def _build_track_json_response(self, name, artist_name, total_pages):
        return { 
            'recenttracks': { 
                'track': [ 
                    { 
                        'name': name, 
                        'artist': { 
                            'name': artist_name 
                        } 
                    }
                ], 
                '@attr': { 
                    'totalPages': total_pages 
                } 
            } 
        }
