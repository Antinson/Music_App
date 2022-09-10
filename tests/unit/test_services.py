import pytest

from music.tracks import services as services
from music.tracks.services import NonExistentTrackException

def test_can_get_tracks_with_date(in_memory_repo):
    target_date = 2001
    cursor = 0
    tracks_per_page = 19

    track_ids, prev_year, next_year = services.get_track_ids_by_date(target_date, in_memory_repo)
    tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)

    track = in_memory_repo.get_track(track_ids[0])
    assert track.track_id == 642
    assert len(track_ids) == 25
    assert len(tracks) == 19
    assert track_ids[0] == 642
    assert prev_year == 2000
    assert next_year == 2002

    for track in tracks:
        # assert track['album'].release_year == 2006 # should fail
        assert track['album'].release_year == 2001 # should pass

    cursor += tracks_per_page
    # cursor change, show next 19 tracks
    tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)
    assert tracks[0]['track_id'] == 3580
    assert len(track_ids) == 25
    assert len(tracks) == 6
    assert track_ids[19] == 3580
    assert prev_year == 2000
    assert next_year == 2002

def test_can_get_tracks_by_album(in_memory_repo):
    target_album_title = 'Awol'


    tracks_by_album_title = services.get_tracks_by_album(target_album_title, in_memory_repo)
    # assert if tracks associated by album == to 2 tracks only
    assert len(tracks_by_album_title) == 4

    # check if track album matches with target album or starts with target album
    for track in tracks_by_album_title:
        assert track['album'].title.lower().startswith(target_album_title.lower())


    # searching by id
    target_album_id = 1
    tracks_by_album = services.get_tracks_by_album(target_album_id, in_memory_repo)
    assert len(tracks_by_album) ==  4

    for track in tracks_by_album:
        assert track['album'].album_id == target_album_id



    # when there are leading and trailing spaces
    target_album_title = 'Awol    '

    tracks_by_album_title = services.get_tracks_by_album(target_album_title, in_memory_repo)
    assert len(tracks_by_album_title) == 4

    for track in tracks_by_album_title:
        assert track['album'].title.lower().startswith('awol')




def test_can_get_tracks_by_artist(in_memory_repo):
    target_artist_name = 'Illusion'


    tracks_by_artist = services.get_tracks_by_artist(target_artist_name, in_memory_repo)
    # assert if tracks associated by album == to 2 tracks only
    assert len(tracks_by_artist) == 15

    # check if track album matches with target album or starts with target album
    for track in tracks_by_artist:
        assert track['artist'].full_name.lower().startswith(target_artist_name.lower())



    # when there are leading and trailing spaces
    target_artist_name = '        Illusion  '

    tracks_by_artist = services.get_tracks_by_artist(target_artist_name, in_memory_repo)
    # assert if tracks associated by album == to 2 tracks only
    assert len(tracks_by_artist) == 15

    # check if track album matches with target album or starts with target album
    for track in tracks_by_artist:
        assert track['artist'].full_name.lower().startswith('illusion')




    # searching by artist id
    target_artist_id = 167
    tracks_by_artist = services.get_tracks_by_artist(target_artist_id, in_memory_repo)

    for track in tracks_by_artist:
        assert track['artist'].artist_id == target_artist_id




def test_can_get_tracks_by_genre(in_memory_repo):
    # searching by genre name, str
    target_genre_name = 'Hip-Hop'

    tracks_by_genre = services.get_tracks_by_genre(target_genre_name, in_memory_repo)
    # assert if tracks associated by genre/s
    assert len(tracks_by_genre) == 41

    # check if tracks_by_genre matches with target genre or starts with target genre
    for track in tracks_by_genre:
        for genre in track['track_genres']:
            assert genre.genre_id == 21



    # when there are leading and trailing spaces
    target_genre_name = '    Hip-Hop  '

    tracks_by_genre = services.get_tracks_by_genre(target_genre_name, in_memory_repo)
    # assert if target_genre_name was stripped
    assert len(tracks_by_genre) == 41

    for track in tracks_by_genre:
        for genre in track['track_genres']:
            assert genre.name == "Hip-Hop"

    # check if tracks_by_genre matches with target genre or starts with target genre
    for track in tracks_by_genre:
        for genre in track['track_genres']:
            assert genre.genre_id == 21



    # searching by genre id
    target_genre_id = 21
    tracks_by_genre_id = services.get_tracks_by_genre(target_genre_id, in_memory_repo)
    assert len(tracks_by_genre_id) == 41

    # check if tracks_by_genre returns a list of dictionaries
    assert type(tracks_by_genre_id) is list
    assert type(tracks_by_genre_id[0]) is dict
    assert tracks_by_genre_id[0]['track_genres'][0].name == 'Hip-Hop' # track_genres is a list

def test_can_get_nav_links(in_memory_repo):
    cursor = 0
    tracks_per_page = 10
    track_ids = services.get_all_track_ids(in_memory_repo)
    tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)

    assert len(track_ids) == 2000

    # checks the first track id which the cursor points to
    assert tracks[0]['track_id'] == 2

    # next iteration
    cursor += tracks_per_page
    track_ids = services.get_all_track_ids(in_memory_repo)
    tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)

    # checks the first track id which the cursor points to
    assert tracks[0]['track_id'] == 135


    # next iteration
    cursor += tracks_per_page
    track_ids = services.get_all_track_ids(in_memory_repo)
    tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], in_memory_repo)

    # checks the first track id which the cursor points to
    assert tracks[0]['track_id'] == 146



