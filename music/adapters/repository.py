import abc
from typing import List
from datetime import date

from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.album import Album
from music.domainmodel.artist import Artist
from music.domainmodel.review import Review
from music.domainmodel.user import User

repo_instance = None


class RepositoryException(Exception):
    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, user_name) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track: Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, id: int) -> Track:
        """
        If there is no Track with the given id, return None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_tracks(self) -> List[Track]:
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_tracks(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_by_date(self, target_date: date) -> List[Track]:
        """
        If there are no Tracks on the given date, return an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_date(self, target_date: date):
        raise NotImplementedError

    @abc.abstractmethod
    def get_dates(self):
        raise NotImplementedError



    @abc.abstractmethod
    def get_first_track(self) -> Track:
        """ Returns the first Track, ordered by date
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_track(self) -> Track:
        """ Returns the last Article, ordered by date, from the repository.

        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_id(self, id_list):
        """ Returns a list of Track, whose ids match those in id_list
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError


    @abc.abstractmethod
    def get_date_of_previous_track(self, track: Track):
        """ If article is the first Tracks in the repository,
        return None because there are no Tracks
        on a previous date.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_date_of_next_track(self, track: Track):
        """ If article is the last Tracks in the repository,
        this method returns None because there are no Tracks
        on a later date.
        """
        raise NotImplementedError
    @abc.abstractmethod
    def get_track_ids_for_genre(self, target_genre: str):
        """ Returns a list of ids representing Tracks
         that are tagged by genre.

        If there are Tracks that are tagged by genre id, return an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_ids_for_artist(self, target_artist: Artist) -> List[Track]:
        """ Returns a list of ids representing Tracks
         that are tagged by artist.

        If there are Tracks that are tagged by artist id, return an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_track_ids_for_album(self, target_album: Album) -> List[Track]:
        """ Returns a list of ids representing Tracks
         that are tagged by album.

        If there are Tracks that are tagged by album id, return an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_album(self, album: Album):
        raise NotImplementedError

    @abc.abstractmethod
    def get_albums(self) -> List[Album]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_artist(self, artist: Artist):
        raise NotImplementedError

    @abc.abstractmethod
    def get_artists(self) -> List[Artist]:
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        raise NotImplementedError


    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Review to the repository.

        If Review doesn't have bidirectional links with a Track,
        this method raises a RepositoryException and doesn't update the repository.
        """

        if review.track is None:
            raise RepositoryException('Review not correctly attached to an Track')

    @abc.abstractmethod
    def get_reviews(self):
        """
         return reviews stored in the repository
        """
        raise NotImplementedError
