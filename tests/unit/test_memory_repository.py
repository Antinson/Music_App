from datetime import date, datetime
from typing import List

import pytest

from music.domainmodel.artist import Artist
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.album import Album
from music.domainmodel.user import User
from music.adapters.csvdatareader import TrackCSVReader

from music.adapters.repository import RepositoryException


class Test_memory_repository:
    def test_repository_can_add_track(self):
        track = Track(44, "Test Song")
        self.add_track(track)

        assert self.get_track(44) is track
