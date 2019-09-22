from src.track import Track


class ScrobbledTrack(Track):
    """Represents a track that has been scrobbled (ie: exists in the user's Last.fm library)"""

    def __init__(self, track_name, artist, playcount):
        super().__init__(track_name, artist)
        self.playcount = playcount

    def __eq__(self, other):
        return isinstance(other, ScrobbledTrack) \
            and self.track_name == other.track_name \
            and self.artist == other.artist \
            and self.playcount == other.playcount

    def __repr__(self):
        return str(self.__dict__)
