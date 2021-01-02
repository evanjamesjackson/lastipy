import unittest
from unittest.mock import patch
from lastipy.lastfm.library.track_info import fetch_playcount
from lastipy.track import Track
from unittest.mock import Mock


class FetchPlaycountTest(unittest.TestCase):

    dummy_track = Track(track_name="Dummy Track", artist="Dummy Artist")

    @patch('requests.get')
    def test_successful_fetch(self, mock_requests_get):
        json_response = {
            'track': {
                'userplaycount': '5'
            }
        }

        mock_response = Mock()
        mock_response.ok = True
        mock_response.json.return_value = json_response
        mock_requests_get.side_effect = [mock_response]

        fetched_playcount = fetch_playcount(track=self.dummy_track, user='dummyUser',
                                            api_key='dummyApiKey')
        self.assertEqual(fetched_playcount, 5)
