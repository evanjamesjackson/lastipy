import unittest
from lastipy.spotify.library import add_albums_to_library
from spotipy import Spotify
from lastipy.spotify.album import SpotifyAlbum

class AddAlbumsToLibraryTest(unittest.TestCase):

    def test_adding_less_than_max_request(self):
        spotify = Spotify()
        spotify.current_user = unittest.mock.MagicMock({'id': 'testUser'})
        spotify.current_user_saved_albums_add = unittest.mock.MagicMock()    
        dummy_albums = [
            SpotifyAlbum('single', '123'),
            SpotifyAlbum('album', '456'),
            SpotifyAlbum('single', '789')
        ]
        add_albums_to_library(spotify, dummy_albums)
        spotify.current_user_saved_albums_add.assert_called_with(['123', '456', '789'])


    def test_adding_more_than_max_request(self):
        spotify = Spotify()
        spotify.current_user = unittest.mock.MagicMock({'id': 'testUser'})
        spotify.current_user_saved_albums_add = unittest.mock.MagicMock()    
       
        dummy_albums = []
        for _ in range(150):
            dummy_albums.append(SpotifyAlbum('single', '123'))
        
        expected_chunks = []
        for _ in range(3):
            chunk = []
            for _ in range(50):
                chunk.append(SpotifyAlbum('single', '123'))
            expected_chunks.append(chunk)

        for i in range(3):
            add_albums_to_library(spotify, expected_chunks[i])
