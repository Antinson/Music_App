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

    def get_all_tracks(self):
        return self.__tracks

    def get_number_of_tracks(self) -> int:
        return len(self.__tracks)

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

    def get_date_of_previous_track(self, track: Track):
        previous_date = None

        try:
            index = self.track_index(track)
            for stored_track in reversed(self.__tracks[0:index]):
                if stored_track.date < track.date:
                    previous_date = stored_track.date
                    break
        except ValueError:
            pass

    def get_date_of_next_track(self, track: Track):
        next_date = None

        try:
            index = self.track_index(track)
            for stored_track in self.__tracks[index + 1: len(self.__tracks)]:
                if stored_track.date > track.date:
                    next_date = stored_track.date
                    break
        except ValueError:
            pass
        return next_date

    def get_track_ids_for_genre(self, target_genre: str) -> List[Track]:
        genre = next((genre for genre in self.__genres if target_genre == genre.name))

        if genre is not None:
            track_ids = list()
            for track in self.__tracks:
                if genre in track.genres:
                    track_ids.append(track.track_id)

        else:
            track_ids = list()
        return track_ids

    def get_track_ids_for_artist(self, target_artist: str) -> List[Track]:
        artist = next((artist for artist in self.__artists if target_artist in artist.full_name))

        if artist is not None:
            track_ids = list()
            for track in self.__tracks:
                if track.artist == artist:
                    track_ids.append(track.track_id)

        else:
            track_ids = list()
        return track_ids

    def get_track_ids_for_album(self, target_album: str) -> List[Track]:
        album = next((album for album in self.__albums if target_album in album.title))

        if album is not None:
            track_ids = list()
            for track in self.__tracks:
                if track.artist == album:
                    track_ids.append(track.track_id)

        else:
            track_ids = list()
        return track_ids


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



    def add_review(self, review: Review):
        # call parent
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

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
