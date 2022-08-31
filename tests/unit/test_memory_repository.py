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




def test_repository_can_get_track_count(in_memory_repo):
    number_of_tracks = in_memory_repo.get_number_of_tracks()
    assert number_of_tracks == 2000


def test_repository_can__add_track(in_memory_repo):
    track = Track(1, "Test SoOo0nnng")
    in_memory_repo.add_track(track)

def test_repository_can_get_track(in_memory_repo):
    track = in_memory_repo.get_track(2)

    assert track.album.album_id == 1

    assert track.artist.artist_id == 1
    assert track.artist.full_name == "AWOL"

    # todo
    # maybe check if track has a comment made by user
    # and if genres that are associated are correct

def test_does_not_get_non_existent_track(in_memory_repo):
    track = in_memory_repo.get_track(4000)
    assert track is None

