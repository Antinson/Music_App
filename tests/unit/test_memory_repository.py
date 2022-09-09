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

def test_repository_does_not_get_non_existent_track(in_memory_repo):
    track = in_memory_repo.get_track(4000)
    assert track is None

def test_repository_can_get_track_id_for_existing_genre(in_memory_repo):
    track_ids = in_memory_repo.get_track_ids_for_genre('Hip-Hop')
    assert track_ids == [2, 3, 5, 134, 583, 584, 585, 586, 668, 669, 670, 671, 672,
                         673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683,
                         684, 685, 686, 687, 688, 689, 694, 695, 3316, 3317, 3318,
                         3319, 3320, 3321, 3322, 3323, 3324]

def test_repository_can_get_tracks_of_certain_date(in_memory_repo):
    target_date = 2001
    tracks = in_memory_repo.get_track_by_date(target_date)

    for track in tracks:
        assert track.album.release_year == 2001

    assert len(tracks) == 25

def test_repository_can_previous_date_of_track(in_memory_repo):
    tracks_of_oldest_date = in_memory_repo.get_track_by_date(1981)
    tracks_of_earliest_date = in_memory_repo.get_track_by_date(2009)
    tracks_of_date_in_between = in_memory_repo.get_track_by_date(2001)

    prev_date = in_memory_repo.get_date_of_previous_track(tracks_of_oldest_date[0])
    next_date = in_memory_repo.get_date_of_next_track(tracks_of_oldest_date[0])

    assert prev_date == None
    assert next_date == 1982

    prev_date = in_memory_repo.get_date_of_previous_track(tracks_of_earliest_date[0])
    next_date = in_memory_repo.get_date_of_next_track(tracks_of_earliest_date[0])

    assert prev_date == 2008
    assert next_date == None

    prev_date = in_memory_repo.get_date_of_previous_track(tracks_of_date_in_between[0])
    next_date = in_memory_repo.get_date_of_next_track(tracks_of_date_in_between[0])

    assert prev_date == 2000
    assert next_date == 2002

def test_dates_list(in_memory_repo):
    dates = in_memory_repo.get_dates()
    assert dates == [1, 2]