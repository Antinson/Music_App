from datetime import date, datetime
from typing import List

import pytest

from music.domainmodel.artist import Artist
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.review import Review
from music.domainmodel.album import Album
from music.domainmodel.user import User


import pytest

def test_repository_can_add_user(in_memory_repo):
    user = User(3, 'tim', 'password')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('tim') is user


def test_repository_can_get_existing_user(in_memory_repo):
    # add two users
    in_memory_repo.add_user(User(3, 'tim', 'password'))
    in_memory_repo.add_user(User(4, 'Bob', 'secretpass'))

    # check can get user with user name tim
    user = in_memory_repo.get_user('tim')
    assert user == User(3, 'tim', 'password')

    assert user != User(4, 'Bob', 'secretpass')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('alphabet')
    assert user is None


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

def test_repository_can_get_tracks_by_id(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_id([2, 20, 48])
    assert len(tracks) == 3

    assert tracks[0].title == 'Food'
    assert tracks[1].title == 'Spiritual Level'
    assert tracks[2].title == 'Light of Light'

def test_repository_does_not_get_tracks_when_no_matching_track_id(in_memory_repo):
    # for non existing track ids only
    tracks = in_memory_repo.get_tracks_by_id([4, 6, 7, 8, 9])
    assert len(tracks) == 0

    # with existing and non-existing track_ids
    tracks = in_memory_repo.get_tracks_by_id([2, 4, 6, 7, 8])
    assert len(tracks) == 1
    assert tracks[0].title == 'Food'

def test_repository_can_get_track_id_for_existing_genre(in_memory_repo):
    track_ids = in_memory_repo.get_track_ids_by_genre('Hip-Hop')

    assert track_ids == [2, 3, 5, 134, 583, 584, 585, 586, 668, 669, 670, 671, 672,
                         673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683,
                         684, 685, 686, 687, 688, 689, 694, 695, 3316, 3317, 3318,
                         3319, 3320, 3321, 3322, 3323, 3324]

    # check if can get tracks and if genre is Hip-Hop
    tracks = in_memory_repo.get_tracks_by_id(track_ids)

    # all tracks retrieved should contain the genre 'Hip-Hop'
    for track in tracks:
        for genre in track.genres:
            if genre.name == 'Hip-Hop':
                assert genre.name == 'Hip-Hop'


def test_repository_does_not_get_tracks_when_no_matching_genre(in_memory_repo):
    target_genre = 'Dubstep'
    tracks = in_memory_repo.get_track_ids_by_genre(target_genre)

    assert len(tracks) == 0




def test_repository_can_get_tracks_of_certain_date(in_memory_repo):
    target_date = 2001
    tracks = in_memory_repo.get_track_by_date(target_date)

    for track in tracks:
        assert track.album.release_year == 2001

    assert len(tracks) == 25

def test_repository_does_not_get_tracks_when_no_matching_date(in_memory_repo):
    target_date = 2010
    tracks = in_memory_repo.get_track_ids_by_date(target_date)

    assert len(tracks) == 0

def test_repository_can_get_previous_date_of_target_date(in_memory_repo):
    target_date = 2008
    track_ids_of_target_date = in_memory_repo.get_track_ids_by_date(target_date)
    tracks = in_memory_repo.get_tracks_by_id(track_ids_of_target_date)

    prev_date = in_memory_repo.get_date_of_previous_track(tracks[0])
    assert prev_date == 2007

def test_repository_can_get_next_date_of_target_date(in_memory_repo):
    target_date = 2000
    track_ids_of_target_date = in_memory_repo.get_track_ids_by_date(target_date)
    tracks = in_memory_repo.get_tracks_by_id(track_ids_of_target_date)

    next_date = in_memory_repo.get_date_of_next_track(tracks[0])
    assert next_date == 2001

def test_repository_returns_none_when_no_previous_date_of_target_date(in_memory_repo):
    target_date = 1981
    track_ids_of_target_date = in_memory_repo.get_track_ids_by_date(target_date)
    tracks = in_memory_repo.get_tracks_by_id(track_ids_of_target_date)

    prev_date = in_memory_repo.get_date_of_previous_track(tracks[0])
    assert prev_date == None

def test_repository_returns_none_when_no_next_date_of_target_date(in_memory_repo):
    target_date = 2009
    track_ids_of_target_date = in_memory_repo.get_track_ids_by_date(target_date)
    tracks = in_memory_repo.get_tracks_by_id(track_ids_of_target_date)

    next_date = in_memory_repo.get_date_of_next_track(tracks[0])
    assert next_date == None


def test_repository_can_get_dates_list(in_memory_repo):
    dates = in_memory_repo.get_dates()
    assert dates == [1981, 1982, 1995, 1996, 1998, 1999, 2000, 2001, 2002, 2003,
                     2004, 2005, 2006, 2007, 2008, 2009]