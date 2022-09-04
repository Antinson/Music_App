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

def add_review(track_id: int, comment_text: str, user_name: str, rating: int, repo: AbstractRepository):

    
    # Check that the track exists.
    track = repo.get_track(track_id)
    print(track)

    # Get the current user that commented
    user = repo.get_user(user_name.lower())
    print(user)

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
    track.genres = dict.track_genres

    return track

def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]
