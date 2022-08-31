import csv
from pathlib import Path
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.artist import Artist
from music.domainmodel.review import Review
from music.domainmodel.user import User
from music.domainmodel.album import Album
from music.adapters.csvdatareader import TrackCSVReader


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self.__tracks = list()
        self.__tracks_index = dict()
        self.__genres = list()
        self.__albums = list()
        self.__users = list()
        self.__reviews = list()
        self.__artists = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def add_track(self, track: Track):
        insort_left(self.__tracks, track)
        self.__tracks_index[track.track_id] = track

    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self.__tracks_index[id]
        except KeyError:
            pass
        return track

    def get_track_by_date(self, target_date: date) -> List[Track]:
        # set the temporary track and album to have the target date
        target_track = Track(track_id=None, track_title=None)
        album_with_target_date = Album(album_id=None, title=None)
        album_with_target_date.release_year = target_date
        target_track.album = album_with_target_date

        matching_tracks = list()

        try:
            index = self.track_index(target_track)
            for track in self.__tracks[index: None]:
                if track.album.release_year == target_date:
                    matching_tracks.append(track)
                else:
                    break
        except ValueError:
            pass

        return matching_tracks

    def get_number_of_tracks(self) -> int:
        return len(self.__tracks)

    def get_first_track(self) -> Track:
        track = None

        if len(self.__tracks) > 0:
            track = self.__tracks[0]
        return track

    def get_last_track(self) -> Track:
        track = None

        if len(self.__tracks) > 0:
            track = self.__tracks[-1]
        return track

    def get_tracks_by_id(self, id_list):
        existing_ids = [id for id in id_list if id in self.__tracks_index]
        tracks = [self.__tracks_index[id] for id in existing_ids]
        return tracks

    def get_track_ids_for_genre(self, target_genre: Genre):
        # TODO
        raise NotImplementedError

    def get_date_of_previous_Track(self, track: Track):
        # TODO
        """ If article is the first Tracks in the repository,
        return None because there are no Tracks
        on a previous date.
        """
        raise NotImplementedError

    def get_date_of_next_article(self, track: Track):
        # TODO
        """ If article is the last Tracks in the repository,
        this method returns None because there are no Tracks
        on a later date.
        """
        raise NotImplementedError

    def add_album(self, album: Album):
        self.__albums.append(album)

    def get_albums(self) -> List[Album]:
        return self.__albums

    def add_artist(self, artist: Artist):
        self.__artists.append(artist)

    def get_artists(self) -> List[Artist]:
        return self.__artists

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def get_genres(self) -> List[Genre]:
        return self.__genres

    def get_track_by_artist(self, target_artist: Artist) -> List[Track]:
        """ Returns a list of Tracks by artist
        If there are no Tracks by given artist, return None.
        """

    def add_review(self, review: Review):
        # TODO
        """ Adds a Review to the repository.

        If Review doesn't have bidirectional links with a Track,
        this method raises a RepositoryException and doesn't update the repository.
        """

        if review.track is None:
            raise RepositoryException('Review not correctly attached to an Track')

    def get_reviews(self):
        # TODO
        raise NotImplementedError

    def track_index(self, track: Track):
        index = bisect_left(self.__tracks, track)
        if index != len(self.__tracks) and self.__tracks[index].album.release_year == track.album.release_year:
            return index
        raise ValueError


def load_tracks_and_album(data_path: Path, repo: MemoryRepository):
    albums_file_name = str(Path(data_path) / 'raw_albums_excerpt.csv')
    tracks_file_name = str(Path(data_path) / 'raw_tracks_excerpt.csv')
    reader = TrackCSVReader(albums_file_name, tracks_file_name)
    reader.read_csv_files()

    for track in reader.dataset_of_tracks:
        repo.add_track(track)

    for album in reader.dataset_of_albums:
        repo.add_album(album)

    for artist in reader.dataset_of_artists:
        repo.add_artist(artist)

    for genre in reader.dataset_of_genres:
        repo.add_genre(genre)


def populate(data_path: Path, repo: MemoryRepository):
    # Load csv data into the repository.
    load_tracks_and_album(data_path, repo)

    # TODO: load reviews and users