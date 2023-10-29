from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track
from music.domainmodel.review import Review


class NonExistentTrackException(Exception):
    pass


class UnknownUserException(Exception):
    pass


# Used in tracks_browse.py
def get_track(track_id: int, repo: AbstractRepository):
    track = repo.get_track(track_id)
    if track is None:
        raise NonExistentTrackException
    return track_to_dict(track)


def get_all_track_ids(repo: AbstractRepository):
    track_ids = repo.get_all_track_ids()
    track_ids_list = []

    for id in track_ids:
        track_ids_list.append(id)
    return track_ids_list

# Used in both tracks_browse.py and search.py
def get_tracks_by_id(id_list, repo: AbstractRepository):
    tracks = repo.get_tracks_by_id(id_list)
    return tracks_to_dict(tracks)

# Used in search.py
def get_all_dates(repo: AbstractRepository):
    return repo.get_dates()

def get_track_ids_by_track_title(target_track, repo: AbstractRepository):
    if target_track is None or type(target_track) == int:
        raise NonExistentTrackException
    track_ids_by_title = repo.get_track_ids_by_track_title(target_track)
    return track_ids_by_title


def get_track_ids_by_date(date, repo: AbstractRepository):
    track_ids = repo.get_track_ids_by_date(date)

    prev_date = None
    next_date = None

    if len(track_ids) > 0:  # check if there is at least 1 track with specified date
        track = repo.get_track(track_ids[0])
        prev_date = repo.get_date_of_previous_track(track)
        next_date = repo.get_date_of_next_track(track)

    # returns tracks specified by date (Track), prev date and next date(int)
    return track_ids, prev_date, next_date


def get_track_ids_by_album(target_album, repo: AbstractRepository):
    # returns list of track ids that contain the target_album by album id OR album title
    track_ids_by_album = repo.get_track_ids_by_album(target_album)
    return track_ids_by_album


def get_track_ids_by_artist(target_artist, repo: AbstractRepository):
    # returns list of track ids that contain the target_artist by artist id OR artist name
    track_ids_by_artist = repo.get_track_ids_by_artist(target_artist)
    return track_ids_by_artist


def get_track_ids_by_genre(target_genre, repo: AbstractRepository):
    # returns list of track ids that contain target_genre by genre id OR genre name
    track_ids_by_genre = repo.get_track_ids_by_genre(target_genre)
    return track_ids_by_genre


def get_user_liked_tracks(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name.lower())
    return tracks_to_dict(user.liked_tracks)


def add_review(track_id: int, comment_text: str, rating: int, user_name: str, repo: AbstractRepository):
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

# Adds track to users liked tracks
def add_track_to_user(user_name: str, track_id: int, repo: AbstractRepository):
    user = repo.get_user(user_name.lower())
    track = repo.get_track(track_id)
    user.add_liked_track(track)

# Removes track from users liked tracks
def remove_track_from_user(user_name: str, track_id: int, repo: AbstractRepository):
    user = repo.get_user(user_name.lower())
    track = repo.get_track(track_id)
    user.remove_liked_track(track)


def get_reviews_for_track(track_id, repo: AbstractRepository):
    reviews_for_track = [review for review in repo.get_reviews() if review.track.track_id == track_id]
    print(reviews_for_track)

    return reviews_to_dict(reviews_for_track)




# ============================================
# Functions to convert model entities to dicts
# ============================================

def track_to_dict(track: Track):
    try:
        track_dict = {
            'track_id': track.track_id,
            'title': track.title,
            'artist': track.artist.to_json(),
            'album': track.album.to_json(),
            'track_url': track.track_url,
            'track_duration': track.track_duration,
            'track_genres': genres_json(track.genres),
            'category_set_to_none': False  # Flag to indicate if category is set to None
        }
    except Exception as e:
        return None

    return track_dict

def genres_json(genres):
    genre_list = []
    for genre in genres:
        genre_list.append(genre.to_json())
    return genre_list

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
