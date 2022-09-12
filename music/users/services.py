from typing import List, Iterable
from music.adapters.repository import AbstractRepository
from music.domainmodel.user import User
from music.domainmodel.review import Review
from music.domainmodel.track import Track

class NameNotUniqueException(Exception):
    pass

class UnknownUserException(Exception):
    pass

class AuthenticationException(Exception):
    pass


def get_user(user_name: str, repo: AbstractRepository):
    return repo.get_user(user_name)

def get_user_reviews(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    return reviews_to_dict(user.reviews)

def get_liked_tracks(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    return tracks_to_dict(user.liked_tracks)


def review_to_dict(review: Review):
    review_dict = {
        'user': review.user,
        'track_id': review.track.track_id,
        'review_text': review.review_text,
        'rating': review.rating,
        'timestamp': review.timestamp
    }

    return review_dict

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

def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]
