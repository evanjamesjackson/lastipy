class Track:
    """Represents a track"""

    def __init__(self, track_name, artist):
        self.track_name = track_name
        self.artist = artist

    def __eq__(self, other):
        return isinstance(other, Track) and self.track_name == other.track_name and self.artist == other.artist

    def __repr__(self):
        return str(self.__dict__)
