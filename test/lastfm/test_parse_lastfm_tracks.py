import unittest
from src.lastfm.parse_lastfm_tracks import parse_tracks


class ParseTracksTest(unittest.TestCase):
    def test_convert_succeeds_with_valid_json(self):
        track_name = "Stayin' Alive"
        artist = "Bee Gees"
        playcount = 5
        to_convert = {
            'name': track_name,
            'artist': {
                'name': artist
            },
            'playcount': str(playcount)
        }

        converted = parse_tracks([to_convert])

        self.assertEqual(converted[0].track_name, track_name)
        self.assertEqual(converted[0].artist, artist)
        self.assertEqual(converted[0].playcount, playcount)

    def test_convert_accounts_for_weird_artist_data(self):
        track_name = "Stayin' Alive"
        artist = "Bee Gees"
        playcount = 5
        to_convert = {
            'name': track_name,
            'artist': {
                'mbid': '45c25199-fa62-4d4c-b0a2-11eeed6923c3',
                '#text': artist
            },
            'playcount': str(playcount)
        }

        converted = parse_tracks([to_convert])

        self.assertEqual(converted[0].track_name, track_name)
        self.assertEqual(converted[0].artist, artist)
        self.assertEqual(converted[0].playcount, playcount)

    def test_convert_raises_error_with_invalid_json(self):
        invalid_json = {
            'suq': 'madiq'
        }

        # If you make a regular call to your testable function, the error will happen before assertRaises can catch it
        # Passing your test argument(s) directly to assertRaises makes sure things happen in the right sequence
        self.assertRaises(KeyError, parse_tracks, [invalid_json])