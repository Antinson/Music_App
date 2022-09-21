from music.domainmodel.track import Track
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.adapters.repository import RepositoryException

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


def test_repository_can_get_all_track_ids(in_memory_repo):
    track_ids = in_memory_repo.get_all_track_ids()
    assert len(track_ids) == 2000


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


def test_repository_can_get_track_ids_for_existing_genre(in_memory_repo):
    target_genre = 'Hip-Hop'
    track_ids = in_memory_repo.get_track_ids_by_genre(target_genre)

    assert track_ids == [2, 3, 5, 134, 583, 584, 585, 586, 668, 669, 670, 671, 672,
                         673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683,
                         684, 685, 686, 687, 688, 689, 694, 695, 3316, 3317, 3318,
                         3319, 3320, 3321, 3322, 3323, 3324]

    # check if can get tracks and if genre is Hip-Hop
    tracks = in_memory_repo.get_tracks_by_id(track_ids)

    # all tracks retrieved should contain the genre 'Hip-Hop'
    for track in tracks:
        for genre in track.genres:
            if genre.name == target_genre:
                assert genre.name == target_genre


def test_repository_does_not_get_track_ids_when_no_matching_genre(in_memory_repo):
    target_genre = 'Dubstep'
    track_ids = in_memory_repo.get_track_ids_by_genre(target_genre)

    assert len(track_ids) == 0


def test_repository_can_get_track_ids_for_existing_album(in_memory_repo):
    target_album = 'Niris'
    track_ids = in_memory_repo.get_track_ids_by_album(target_album)
    tracks = in_memory_repo.get_tracks_by_id(track_ids)

    for track in tracks:
        assert track.album.title == target_album


def test_repository_does_not_get_track_ids_when_no_matching_album(in_memory_repo):
    target_album = 'My Newest Album'
    track_ids = in_memory_repo.get_track_ids_by_album(target_album)

    assert len(track_ids) == 0


def test_repository_can_get_track_ids_for_existing_artist(in_memory_repo):
    target_artist = 'Area C'
    track_ids = in_memory_repo.get_track_ids_by_artist(target_artist)

    assert len(track_ids) == 13

    tracks = in_memory_repo.get_tracks_by_id(track_ids)

    for track in tracks:
        assert track.artist.full_name == target_artist


def test_repository_does_not_get_track_ids_when_no_matching_artist(in_memory_repo):
    target_artist = 'New Jeans'
    track_ids = in_memory_repo.get_track_ids_by_artist(target_artist)

    assert len(track_ids) == 0


def test_repository_can_get_track_ids_for_exsisting_track_title(in_memory_repo):
    target_track_title = 'The  '
    track_ids = in_memory_repo.get_track_ids_by_track_title(target_track_title)

    # check how many tracks starts with 'The' as their track title
    assert len(track_ids) == 95

    tracks = in_memory_repo.get_tracks_by_id(track_ids)
    target_track_title = target_track_title.strip().lower()  # 'the'
    for track in tracks:
        assert track.title.lower().startswith(target_track_title)


def test_repository_does_not_get_track_ids_when_no_matching_track_title(in_memory_repo):
    target_track_title = 'Pencil '
    track_ids = in_memory_repo.get_track_ids_by_track_title(target_track_title)
    assert len(track_ids) == 0


def test_repository_can_get_tracks_of_certain_date(in_memory_repo):
    target_date = 2001
    track_ids_of_target_date = in_memory_repo.get_track_ids_by_date(target_date)
    tracks = in_memory_repo.get_tracks_by_id(track_ids_of_target_date)

    assert len(track_ids_of_target_date) == 25

    for track in tracks:
        assert track.album.release_year == 2001




def test_repository_does_not_get_tracks_when_no_matching_date(in_memory_repo):
    target_date = 2010
    track_ids = in_memory_repo.get_track_ids_by_date(target_date)

    assert len(track_ids) == 0


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
    assert prev_date is None


def test_repository_returns_none_when_no_next_date_of_target_date(in_memory_repo):
    target_date = 2009
    track_ids_of_target_date = in_memory_repo.get_track_ids_by_date(target_date)
    tracks = in_memory_repo.get_tracks_by_id(track_ids_of_target_date)

    next_date = in_memory_repo.get_date_of_next_track(tracks[0])
    assert next_date is None


def test_repository_can_add_date(in_memory_repo):
    date = 2022
    in_memory_repo.add_date(date)
    stored_dates = in_memory_repo.get_dates()
    assert date in stored_dates


def test_repository_get_all_stored_dates(in_memory_repo):
    dates = in_memory_repo.get_dates()
    assert dates == [1981, 1982, 1995, 1996, 1998, 1999, 2000, 2001, 2002, 2003,
                     2004, 2005, 2006, 2007, 2008, 2009]


def test_repository_can_add_review(in_memory_repo):
    user = User(3, 'Tim', 'password')
    track = in_memory_repo.get_track(1270)

    review = Review(track, 'this song is so good!', 5, user.user_name)
    in_memory_repo.add_review(review)

    reviews = in_memory_repo.get_reviews()

    # check if review made is added
    assert review in reviews


def test_repository_can_get_reviews(in_memory_repo):
    user = User(3, 'Tim', 'password')

    track = in_memory_repo.get_track(1270)
    review = Review(track, 'this song is so good!', 5, user.user_name)
    in_memory_repo.add_review(review)

    track = in_memory_repo.get_track(140)
    review = Review(track, 'mid', 2, user.user_name)
    in_memory_repo.add_review(review)

    user = User(4, 'Jewel', 'secret')
    track = in_memory_repo.get_track(20)
    review = Review(track, 'nice :)', 4, user.user_name)
    in_memory_repo.add_review(review)

    # check total reviews made
    reviews = in_memory_repo.get_reviews()
    assert len(reviews) == 3


def test_repository_does_not_add_review_without_proper_user_and_review_attachment(in_memory_repo):
    track = in_memory_repo.get_track(1270)
    review = Review(track, 'made me cry', 5, None)

    # check if error is raised bc the review has no user
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)

def test_repository_does_not_add_review_without_proper_track_and_review_attachment(in_memory_repo):
    user = User(4, 'Jewel', 'secret')
    review = Review(None, 'made me cry', 5, 'jewel')

    user.add_review(review)

    # checks if exception is raised bc the review does not refer to a Track
    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)
