from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track
from music.domainmodel.review import Review


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
    # returns list of track ids that contain the target_album by album id OR album title
    track_ids_by_album = repo.get_track_ids_by_album(target_album)

    # gets the tracks by album/s
    tracks_by_album = repo.get_tracks_by_id(track_ids_by_album)
    return tracks_to_dict(tracks_by_album)


def get_tracks_by_artist(target_artist, repo: AbstractRepository):
    # returns list of track ids that contain the target_artist by artist id OR artist name
    track_ids_by_artist = repo.get_track_ids_by_artist(target_artist)

    # gets the tracks by matching artist/s
    tracks_by_artist = repo.get_tracks_by_id(track_ids_by_artist)
    return tracks_to_dict(tracks_by_artist)


def get_tracks_by_genre(target_genre, repo: AbstractRepository):
    # returns list of track ids that contain target_genre by genre id OR genre name
    track_ids_by_genre = repo.get_track_ids_by_genre(target_genre)

    # gets the tracks by matching genres/s
    tracks_by_genre = repo.get_tracks_by_id(track_ids_by_genre)
    return tracks_to_dict(tracks_by_genre)


def get_genres(repo: AbstractRepository):
    return repo.get_genres()


def get_albums(repo: AbstractRepository):
    return repo.get_albums()


def get_artists(repo: AbstractRepository):
    return repo.get_artists()

def add_review(track_id: int, comment_text: str, user_name: str, rating: int, repo: AbstractRepository):

    
    # Check that the track exists.
    track = repo.get_track(track_id)

    # Get the current user that commented
    user = repo.get_user(user_name.lower())

    # Create a review object
    review = Review(track, comment_text, rating, user_name)

    # Add the review to user's reviews
    user.add_review(review)

    # Update our repository
    repo.add_review(review)

def get_reviews_for_track(track_id, repo: AbstractRepository):
    
    reviews_for_track = [review for review in repo.get_reviews() if review.track.track_id == track_id]

    return reviews_to_dict(reviews_for_track)


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

def review_to_dict(review: Review):
    review_dict = {
        'user': review.user,
        'track_id': review.track.track_id,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }

    return review_dict


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]


def dict_to_track(dict):
    track = Track(dict.track_id, dict.title)
    track.artist = dict.artist
    track.album = dict.album
    track.track_url = dict.track_url
    track.track_duration = dict.track_duration
    for genre in dict.track_genres:
        track.add_genre(genre)

    return track

def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]
