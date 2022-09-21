from music.tracks import services as tracks_services
from music.authentication import services as auth_services
from music.users import services as user_services

from music.domainmodel.user import User


import pytest
from music.tracks.services import NonExistentTrackException


# Authentication
def test_authentication_can_add_user(in_memory_repo):
    user_name = 'jewel'
    password = 'secret'

    auth_services.add_user(user_name, password, in_memory_repo)
    user_dict = auth_services.get_user('jewel', in_memory_repo)
    assert user_dict['user_name'] == user_name

    # check password is encrypted
    assert user_dict['password'].startswith('pbkdf2:sha256:')


def test_authentication_cannot_add_user_with_existing_name(in_memory_repo):
    auth_services.add_user('jewel', 'secret', in_memory_repo)

    user_name = 'jewel'
    password = 'password'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_auth_with_valid_credentials(in_memory_repo):
    user_name = 'tim'
    password = 'lobster123'

    auth_services.add_user(user_name, password, in_memory_repo)

    try:
        auth_services.authenticate_user(user_name, password, in_memory_repo)
    except auth_services.AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    user_name = 'tim'
    password = 'lobster123'

    auth_services.add_user(user_name, password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(user_name, 'password', in_memory_repo)

def test_can_get_all_dates(in_memory_repo):
    dates = tracks_services.get_all_dates(in_memory_repo)
    assert dates == [1981, 1982, 1995, 1996, 1998, 1999, 2000, 2001, 2002, 2003,
                     2004, 2005, 2006, 2007, 2008, 2009]

def test_can_get_user(in_memory_repo):
    user_name = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name, password, in_memory_repo)

    user = user_services.get_user(user_name, in_memory_repo)
    assert type(user) == User

    assert user.user_name == user_name


def test_can_get_user_reviews(in_memory_repo):
    # user
    user_name = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name, password, in_memory_repo)

    # create review
    tracks_services.add_review(1270, 'Made me cry', 5, user_name, in_memory_repo)
    tracks_services.add_review(20, 'my back broke bc of diz songk', 1, user_name, in_memory_repo)

    reviews = user_services.get_user_reviews(user_name, in_memory_repo)

    assert len(reviews) == 2


def test_can_get_liked_tracks(in_memory_repo):
    # user
    user_name = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name, password, in_memory_repo)

    liked_tracks = user_services.get_liked_tracks(user_name, in_memory_repo)
    assert len(liked_tracks) == 0

    # add a couple of liked tracks
    tracks_services.add_track_to_user(user_name, 1270, in_memory_repo)
    tracks_services.add_track_to_user(user_name, 20, in_memory_repo)

    liked_tracks = user_services.get_liked_tracks(user_name, in_memory_repo)
    assert len(liked_tracks) == 2


def test_can_get_track(in_memory_repo):
    track = tracks_services.get_track(1267, in_memory_repo)
    assert type(track) == dict
    assert track['title'] == 'Clump Clump'
    assert track['artist'].full_name == 'Nautical Almanac'
    assert track['album'].title == 'Cover The Earth'
    assert track['track_url'] == 'http://freemusicarchive.org/music/Nautical_Almanac/Cover_The_Earth/Clump_Clump'
    assert track['track_duration'] == 219


def test_does_not_get_track_that_is_non_exsistent(in_memory_repo):
    with pytest.raises(NonExistentTrackException):
        tracks_services.get_track(4, in_memory_repo)


def test_can_get_all_track_ids(in_memory_repo):
    track_ids = tracks_services.get_all_track_ids(in_memory_repo)
    assert type(track_ids) == list
    assert len(track_ids) == 2000


def test_can_get_track_ids_by_track_title(in_memory_repo):
    track_title = 'Food'
    track_ids = tracks_services.get_track_ids_by_track_title(track_title, in_memory_repo)

    assert len(track_ids) == 2

    # check if tracks in list do match with the target title
    tracks = tracks_services.get_tracks_by_id(track_ids, in_memory_repo)
    for track in tracks:
        assert track['title'] == track_title

    # test if can get tracks that start with 'The '
    track_title = 'The '
    track_ids = tracks_services.get_track_ids_by_track_title(track_title, in_memory_repo)

    assert len(track_ids) == 95

    # check if tracks in list do match with the target title
    tracks = tracks_services.get_tracks_by_id(track_ids, in_memory_repo)
    for track in tracks:
        assert track['title'].lower().startswith(track_title.strip().lower())


def test_does_not_return_track_ids_when_no_matching_track_title(in_memory_repo):
    track_title = 'non existent track title'
    track_ids = tracks_services.get_track_ids_by_track_title(track_title, in_memory_repo)

    assert len(track_ids) == 0

    track_title = 5
    with pytest.raises(NonExistentTrackException):
        tracks_services.get_track_ids_by_track_title(track_title, in_memory_repo)


def test_can_get_tracks_with_date(in_memory_repo):
    target_date = 2001
    cursor = 0
    tracks_per_page = 19

    track_ids, prev_year, next_year = tracks_services.get_track_ids_by_date(target_date, in_memory_repo)
    tracks = tracks_services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)

    track = in_memory_repo.get_track(track_ids[0])
    assert track.track_id == 642
    assert len(track_ids) == 25
    assert len(tracks) == 19
    assert track_ids[0] == 642
    assert prev_year == 2000
    assert next_year == 2002

    for track in tracks:
        # assert track['album'].release_year == 2006 # should fail
        assert track['album'].release_year == 2001  # should pass

    cursor += tracks_per_page
    # cursor change, show next 19 tracks
    tracks = tracks_services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)
    assert tracks[0]['track_id'] == 3580
    assert len(track_ids) == 25
    assert len(tracks) == 6
    assert track_ids[19] == 3580
    assert prev_year == 2000
    assert next_year == 2002


def test_does_not_get_track_ids_when_no_matches_by_date(in_memory_repo):
    target_date = 2022
    track_ids, prev_date, next_date = tracks_services.get_track_ids_by_date(target_date, in_memory_repo)

    assert len(track_ids) == 0
    assert prev_date is None
    assert next_date is None


def test_can_get_tracks_by_album_title(in_memory_repo):
    target_album_title = 'Awol'

    track_ids = tracks_services.get_track_ids_by_album(target_album_title, in_memory_repo)
    assert len(track_ids) == 4

    tracks = tracks_services.get_tracks_by_id(track_ids, in_memory_repo)

    # check if track album matches with target album or starts with target album
    for track in tracks:
        assert track['album'].title.lower().startswith(target_album_title.lower())

    # when there are leading and trailing spaces
    target_album_title = 'Awol    '

    track_ids = tracks_services.get_track_ids_by_album(target_album_title, in_memory_repo)
    assert len(track_ids) == 4

    tracks = tracks_services.get_tracks_by_id(track_ids, in_memory_repo)

    for track in tracks:
        assert track['album'].title.lower().startswith(target_album_title.strip().lower())


def test_does_not_get_track_ids_when_no_matching_album(in_memory_repo):
    target_album_title = 'non existent album'
    track_ids = tracks_services.get_track_ids_by_album(target_album_title, in_memory_repo)

    assert len(track_ids) == 0


def test_can_get_tracks_by_artist_name(in_memory_repo):
    target_artist_name = 'Illusion'

    track_ids = tracks_services.get_track_ids_by_artist(target_artist_name, in_memory_repo)
    assert len(track_ids) == 15

    tracks = tracks_services.get_tracks_by_id(target_artist_name, in_memory_repo)

    # check if track album matches with target album or starts with target album
    for track in tracks:
        assert track['artist'].full_name.lower().startswith(target_artist_name.lower())

    # when there are leading and trailing spaces
    target_artist_name = '        Illusion  '

    track_ids = tracks_services.get_track_ids_by_artist(target_artist_name, in_memory_repo)
    assert len(track_ids) == 15

    tracks = tracks_services.get_tracks_by_id(target_artist_name, in_memory_repo)

    # check if track album matches with target album or starts with target album
    for track in tracks:
        assert track['artist'].full_name.lower().startswith(target_artist_name.strip().lower())


def test_does_not_get_track_ids_when_no_matching_artist(in_memory_repo):
    target_artist_name = 'non existent artist'

    track_ids = tracks_services.get_track_ids_by_artist(target_artist_name, in_memory_repo)
    assert len(track_ids) == 0


def test_can_get_tracks_by_genre_name(in_memory_repo):
    target_genre_name = '     Hip-Hop'

    track_ids = tracks_services.get_track_ids_by_genre(target_genre_name, in_memory_repo)
    assert len(track_ids) == 41

    tracks = tracks_services.get_tracks_by_id(track_ids, in_memory_repo)

    # check if tracks_by_genre matches with target genre
    for track in tracks:
        for genre in track['track_genres']:
            assert genre.genre_id == 21
            assert genre.name == target_genre_name.strip()


    target_genre_name = '     B'

    track_ids = tracks_services.get_track_ids_by_genre(target_genre_name, in_memory_repo)
    assert len(track_ids) == 41

    tracks = tracks_services.get_tracks_by_id(track_ids, in_memory_repo)

    # check if tracks_by_genre matches with target genre
    for track in tracks:
        for genre in track['track_genres']:
            if genre.name.startswith(target_genre_name.strip()):
                assert genre.name.startswith(target_genre_name.strip())

def test_does_not_get_track_ids_when_no_matching_genre(in_memory_repo):
    target_genre_name = 'non existent genre'
    track_ids = tracks_services.get_track_ids_by_genre(target_genre_name, in_memory_repo)

    assert len(track_ids) == 0


def test_can_get_correct_slicing_for_display(in_memory_repo):
    cursor = 0
    tracks_per_page = 10
    track_ids = tracks_services.get_all_track_ids(in_memory_repo)
    tracks = tracks_services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)

    assert len(track_ids) == 2000

    # checks the first track id which the cursor points to
    assert tracks[0]['track_id'] == 2

    # next iteration
    cursor += tracks_per_page
    track_ids = tracks_services.get_all_track_ids(in_memory_repo)
    tracks = tracks_services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)

    # checks the first track id which the cursor points to
    assert tracks[0]['track_id'] == 135

    # next iteration
    cursor += tracks_per_page
    track_ids = tracks_services.get_all_track_ids(in_memory_repo)
    tracks = tracks_services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)

    # checks the first track id which the cursor points to
    assert tracks[0]['track_id'] == 146


def test_can_add_review(in_memory_repo):
    # user
    user_name = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name, password, in_memory_repo)

    tracks_services.add_review(1270, 'Made me cry', 5, user_name, in_memory_repo)

    reviews = tracks_services.get_reviews_for_track(1270, in_memory_repo)
    assert len(reviews) == 1

    for review in reviews:
        assert review['review_text'] == 'Made me cry'
        assert review['user'] == user_name


def test_can_add_liked_track_to_user(in_memory_repo):
    # user
    user_name = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name, password, in_memory_repo)

    tracks_services.add_track_to_user(user_name, 1270, in_memory_repo)
    tracks_services.add_track_to_user(user_name, 2, in_memory_repo)
    tracks_services.add_track_to_user(user_name, 20, in_memory_repo)

    liked_tracks = tracks_services.get_user_liked_tracks(user_name, in_memory_repo)
    assert len(liked_tracks) == 3

def test_does_not_add_non_existent_tracks_to_liked_tracks_of_user(in_memory_repo):
    # user
    user_name = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name, password, in_memory_repo)

    tracks_services.add_track_to_user(user_name, 1270, in_memory_repo)
    tracks_services.add_track_to_user(user_name, 2, in_memory_repo)
    # non existent track
    tracks_services.add_track_to_user(user_name, 4, in_memory_repo)

    liked_tracks = tracks_services.get_user_liked_tracks(user_name, in_memory_repo)
    assert len(liked_tracks) == 2



def test_can_remove_track_from_liked_tracks_of_user(in_memory_repo):
    # user
    user_name = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name, password, in_memory_repo)

    # initialise liked_tracks
    tracks_services.add_track_to_user(user_name, 1270, in_memory_repo)
    tracks_services.add_track_to_user(user_name, 2, in_memory_repo)
    tracks_services.add_track_to_user(user_name, 20, in_memory_repo)

    # remove a track from liked_tracks of user
    tracks_services.remove_track_from_user(user_name, 2, in_memory_repo)

    liked_tracks = tracks_services.get_user_liked_tracks(user_name, in_memory_repo)
    assert len(liked_tracks) == 2



def test_does_not_change_liked_tracks_when_removing_non_existent_track_from_user(in_memory_repo):
    # user
    user_name = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name, password, in_memory_repo)

    # initialise liked_tracks
    tracks_services.add_track_to_user(user_name, 1270, in_memory_repo)
    tracks_services.add_track_to_user(user_name, 2, in_memory_repo)
    tracks_services.add_track_to_user(user_name, 20, in_memory_repo)

    liked_tracks = tracks_services.get_user_liked_tracks(user_name, in_memory_repo)
    assert len(liked_tracks) == 3

    # remove non existent track
    tracks_services.remove_track_from_user(user_name, 5, in_memory_repo)
    liked_tracks = tracks_services.get_user_liked_tracks(user_name, in_memory_repo)
    assert len(liked_tracks) == 3

def test_can_get_reviews_for_a_track(in_memory_repo):
    # user tim
    user_name_tim = 'tim'
    password = 'lobster123'
    auth_services.add_user(user_name_tim, password, in_memory_repo)

    # user jewel
    user_name_jewel = 'jewel'
    password = 'secret243'
    auth_services.add_user(user_name_jewel, password, in_memory_repo)

    # add reviews to track 1270
    tracks_services.add_review(1270, 'spicy yum', 5, user_name_tim, in_memory_repo)
    tracks_services.add_review(1270, 'worst song ever!! >:(', 1, user_name_jewel, in_memory_repo)

    # reviews of track 1270
    reviews = tracks_services.get_reviews_for_track(1270, in_memory_repo)
    assert len(reviews) == 2

    assert reviews[0]['review_text'] == 'spicy yum'
    assert reviews[0]['user'] == user_name_tim

    assert reviews[1]['review_text'] == 'worst song ever!! >:('
    assert reviews[1]['user'] == user_name_jewel
