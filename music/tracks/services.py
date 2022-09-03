from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def get_track(track_id: int, repo: AbstractRepository):
    track = repo.get_track(track_id)
    if track is None:
        raise NonExistentTrackException
    return track_to_dict(track)

def get_all_tracks(repo: AbstractRepository):
    tracks = repo.get_all_tracks()
    return tracks_to_dict(tracks)


def get_first_track(repo: AbstractRepository):  # do we need this?
    track = repo.get_first_track()
    return track_to_dict(track)


def get_last_track(repo: AbstractRepository):  # do we need this?
    track = repo.get_last_track()
    return track_to_dict(track)


def get_tracks_by_date(date, repo: AbstractRepository):
    tracks = repo.get_track_by_date(date)

    prev_date = None
    next_date = None

    if len(tracks) > 0:
        prev_date = repo.get_date_of_previous_track(tracks[0])
        next_date = repo.get_date_of_next_track(tracks[0])

        tracks = tracks_to_dict(tracks)

    return tracks, prev_date, next_date


def get_tracks_by_album(target_album, repo: AbstractRepository):
    track_ids_by_album = repo.get_track_ids_for_album(
        target_album)  # returns list of track ids that contain the target_album
    tracks_by_album = repo.get_tracks_by_id(track_ids_by_album)
    return tracks_to_dict(tracks_by_album)


def get_tracks_by_artist(target_artist, repo: AbstractRepository):
    track_ids_by_artist = repo.get_track_ids_for_artist(target_artist)
    tracks_by_artist = repo.get_tracks_by_id(track_ids_by_artist)
    return tracks_to_dict(tracks_by_artist)


def get_tracks_by_genre(target_genre, repo: AbstractRepository):
    track_ids_by_genre = repo.get_track_ids_for_genre(target_genre)
    tracks_by_genre = repo.get_tracks_by_id(track_ids_by_genre)
    return tracks_to_dict(tracks_by_genre)


def get_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_albums(repo: AbstractRepository):
    return repo.get_albums()


def get_artists(repo: AbstractRepository):
    return repo.get_artists()


# ============================================
# Functions to convert model entities to dicts
# ============================================

def track_to_dict(track: Track):
    track_dict = {
        'track_id': track.track_id,
        'title': track.title,
        'artist': track.artist,
        'album': track.album,
        'track_url': track.track_url,
        'track_duration': track.track_duration,
        'track_genres': track.genres
    }

    return track_dict


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]


def dict_to_track(dict):
    track = Track(dict.track_id, dict.title)
    track.artist = dict.artist
    track.album = dict.album
    track.track_url = dict.track_url
    track.track_duration = dict.track_duration
    track.genres = dict.track_genres

    return track
