import unittest
from src.lastfm import period
from src.lastfm.top_tracks import TopTracksFetcher
from src.lastfm.track import Track
from unittest.mock import patch, Mock
from requests import HTTPError

class TopTracksFetcherTest(unittest.TestCase):
    @patch('requests.get')
    def test_fetch_top_track_success(self, mock_get):
        expected_track = Track(track_name="Stayin' Alive", artist="Bee Gees")

        mock_get.ok = True

        json_track = {
            'name': expected_track.track_name,
                'artist': {
                    'name': expected_track.artist
                }
        }

        first_page_response = {
            'toptracks': {
                'track': [json_track]
            }
        }

        second_page_response = {
            'toptracks': {
                'track': []
            }
        }

        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = first_page_response
        mock_responses[1].json.return_value = second_page_response
        mock_get.side_effect = mock_responses

        fetcher = TopTracksFetcher()
        self.assertEqual(fetcher.fetch_top_tracks(user='sonofjack3', period=period.SEVEN_DAYS)[0], expected_track)
    
    @patch('requests.get')
    def test_fetch_top_track_failure(self, mock_get):
        mock_get.ok = False
        # side_effect will force an error to get thrown when this method gets called
        mock_get.side_effect = HTTPError("Mock")

        fetcher = TopTracksFetcher()
        with self.assertRaises(HTTPError):
            fetcher.fetch_top_tracks('sonofjack3', period.SEVEN_DAYS)

    @patch('requests.get')
    def test_fetch_top_tracks_gets_multiple_tracks(self, mock_get):
        expected_track_1 = Track(track_name="Penny Lane", artist="The Beatles")
        expected_track_2 = Track(track_name="Won't Get Fooled Again", artist="The Who")
        expected_tracks = [expected_track_1, expected_track_2]

        mock_get.ok = True

        json_track_1 =  {
            'name': expected_track_1.track_name,
                'artist': {
                    'name': expected_track_1.artist
                }
        }
        json_track_2 =  {    
            'name': expected_track_2.track_name,
                'artist': {
                    'name': expected_track_2.artist
            }
         
        }

        first_page_response = {
            'toptracks': {
                'track': [json_track_1, json_track_2]
            }
        }

        second_page_response = {
            'toptracks': {
                'track': []
            }
        }

        mock_responses = [Mock(), Mock()]
        mock_responses[0].json.return_value = first_page_response
        mock_responses[1].json.return_value = second_page_response
        mock_get.side_effect = mock_responses

        fetcher = TopTracksFetcher()
        fetched_tracks = fetcher.fetch_top_tracks(user="sonofjack3", period=period.SEVEN_DAYS)
        self.assertCountEqual(fetched_tracks, expected_tracks)