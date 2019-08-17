class Track:
    """Represents a track"""

    def __init__(self, track_name, artist, playcount=1, spotify_id=None):
        self.track_name = track_name
        self.artist = artist
        self.playcount = playcount
        self.spotify_id = spotify_id

    def __eq__(self, other):
        return isinstance(other, Track) \
               and self.track_name == other.track_name \
               and self.artist == other.artist \
               and self.spotify_id == other.spotify_id

    def __repr__(self):
        return str(self.__dict__)
