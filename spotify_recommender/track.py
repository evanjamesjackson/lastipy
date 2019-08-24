class Track:
    """Represents a track"""

    def __init__(self, track_name, artist):
        self.track_name = track_name
        self.artist = artist

    @staticmethod
    def are_equivalent(track_1, track_2):
        return track_1.track_name == track_2.track_name and track_1.artist == track_2.artist

    def __eq__(self, other):
        return isinstance(other, Track) \
               and self.track_name == other.track_name \
               and self.artist == other.artist \

    def __repr__(self):
        return str(self.__dict__)
