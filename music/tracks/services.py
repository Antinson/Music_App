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


def get_first_track(repo: AbstractRepository):
    track = repo.get_first_track()
    return track_to_dict(track)


def get_last_track(repo: AbstractRepository):
    track = repo.get_last_track()
    return track_to_dict(track)


def get_tracks_by_id(id_list, repo: AbstractRepository):
    tracks = repo.get_tracks_by_id(id_list)
    tracks_as_dict = tracks_to_dict(tracks)
    return tracks_as_dict


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
