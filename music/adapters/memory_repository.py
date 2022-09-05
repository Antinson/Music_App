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
        self.__dates = list()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)

    def get_id(self):
        return len(self.__users) + 1

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

    def get_track_by_date(self, target_date: int) -> List[Track]:
        matching_tracks = list()

        for track in self.__tracks:
            if track.album is not None and track.album.release_year is not None:
                track_album_release_year = track.album.release_year
                if track_album_release_year == target_date:
                    matching_tracks.append(track)

        return matching_tracks

    def add_date(self, date: int):
        if date is not None:
            self.__dates.append(date)
            self.__dates.sort()

    def get_dates(self) -> List[int]:
        return self.__dates

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
            index = self.date_index(track.album.release_year)
            for date in reversed(self.__dates[0:index]):
                if date < track.album.release_year:
                    previous_date = date
                    break
        except ValueError:
            pass
        return previous_date

    def get_date_of_next_track(self, track: Track):
        next_date = None
        try:
            index = self.date_index(track.album.release_year)
            for date in self.__dates[index + 1: len(self.__dates)]:
                if date > track.album.release_year:
                    next_date = date
                    break
        except ValueError:
            pass
        return next_date

    def get_track_ids_by_genre(self, target_genre: str) -> List[int]:
        genre = next((genre for genre in self.__genres if target_genre == genre.name))

        if genre is not None:
            track_ids = list()
            for track in self.__tracks:
                if genre in track.genres:
                    track_ids.append(track.track_id)

        else:
            track_ids = list()
        return track_ids

    def get_track_ids_by_artist(self, target_artist: str) -> List[int]:
        artists = list()
        for artist in self.__artists:
            if artist is not None and artist.full_name is not None and target_artist.lower() == artist.full_name.lower() or artist.full_name.lower().startswith(
                    target_artist.lower()):
                artists.append(artist)

        track_ids = list()
        for track in self.__tracks:
            for artist in artists:
                if track.artist == artist:
                    track_ids.append(track.track_id)

        return track_ids

    def get_track_ids_by_artist_id(self, target_artist: int):
        artists = list()
        for artist in self.__artists:
            if artist is not None and artist.artist_id is not None and artist.artist_id == target_artist:
                artists.append(artist)

        track_ids = list()
        for track in self.__tracks:
            for artist in artists:
                if track.artist == artist:
                    track_ids.append(track.track_id)

        return track_ids

    def get_track_ids_by_album(self, target_album: str):
        albums = list()
        for album in self.__albums:
            if album is not None and album.title is not None and target_album.lower() == album.title.lower() or album.title.lower().startswith(target_album.lower()):
                albums.append(album)

        track_ids = list()
        for track in self.__tracks:
            for album in albums:
                if track.album == album:
                    track_ids.append(track.track_id)

        return track_ids

    def get_track_ids_by_album_id(self, target_album: int):
        albums = list()
        for album in self.__albums:
            if album is not None and album.album_id is not None and album.album_id == target_album:
                albums.append(album)

        track_ids = list()
        for track in self.__tracks:
            for album in albums:
                if track.album == album:
                    track_ids.append(track.track_id)

        return track_ids



    def add_album(self, album: Album):
        self.__albums.append(album)
        if album.release_year not in self.__dates:
            self.add_date(album.release_year)

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

    def date_index(self, date: int):
        index = bisect_left(self.__dates, date)
        if index != len(self.__dates) and self.__dates[index] == date:
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
