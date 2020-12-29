class SpotifyAlbum():
    """Represents a Spotify "album". This is slightly confusing in that there are different "types" of albums: albums, and singles."""

    def __init__(self, album_type, spotify_id):
        self.album_type = album_type
        self.spotify_id = spotify_id
    
    def __repr__(self):
        return str(self.__dict__)

SINGLE_ALBUM_TYPE = "single"
ALBUM_ALBUM_TYPE = "album"