from flask import Blueprint, render_template, redirect, url_for, flash, request
import music.tracks.services as services
import music.adapters.repository as repo

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError



search_blueprint = Blueprint('search_bp', __name__, template_folder='templates')

@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if request.method == 'POST':
        return search_by(search_form)

    # For a GET request, return the search page.
    return render_template(
        'tracks/search.html',
        title='Search',
        form=search_form,
        search_target=url_for('search_bp.search')
    )

def search_by(form):
    if (form.search_type.data == 'track'):
        return search_by_track(form.search.data)
    elif (form.search_type.data == 'genre'):
        return search_by_genre(form.search.data)
    elif (form.search_type.data == 'artist'):
        return search_by_artist(form.search.data)
    elif (form.search_type.data == 'date'):
        return search_by_date(form.search.data)
    elif (form.search_type.data == 'album'):
        return search_by_album(form.search.data)

def search_by_album(target_album):
    header = ["Track Id", "Track Name", "Artist", "Album"]
    category = "album"
    # Search for the album.

    tracks_by_album = services.get_tracks_by_album(target_album, repo.repo_instance)
    if len(tracks_by_album) == 0:
        return redirect(url_for('search_bp.not_found'))

    # number of tracks found by target_album
    table_name = str(len(tracks_by_album)) + " results for " + target_album

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_album, category=category)

def search_by_artist(target_artist):
    header = ["Track Id", "Track Name", "Artist", "Album"]
    category = "artist"
    # Search for the artist.

    tracks_by_artist = services.get_tracks_by_artist(target_artist, repo.repo_instance)
    print(tracks_by_artist)
    print(len(tracks_by_artist))
    if len(tracks_by_artist) == 0:
        return redirect(url_for('search_bp.not_found'))

    # number of tracks found by target_artist
    table_name = str(len(tracks_by_artist)) + " results for " + target_artist

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_artist, category=category)

def search_by_date(target_date):
    header = ["Track Id", "Track Name", "Artist", "Length"]
    category = "date"
    # Search for the date.
    print(target_date)

    try:
        tracks, prev_date, next_date = services.get_tracks_by_date(int(target_date), repo.repo_instance)
    except ValueError:
        return redirect(url_for('search_bp.not_found'))

    # number of tracks found by target_date
    table_name = str(len(tracks)) + " results for year " + str(target_date)


    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks, category=category)

def search_by_genre(target_genre):
    header = header = ["Track Id", "Track Name", "Artist", "Album", "Genre Id"]
    category = "genre"
    # Search for the genre.

    tracks_by_genre = services.get_tracks_by_genre(target_genre, repo.repo_instance)
    print(tracks_by_genre[0]['track_genres'])

    if len(tracks_by_genre) == 0:
        return redirect(url_for('search_bp.not_found'))

    # number of tracks found by target_genre
    table_name = str(len(tracks_by_genre)) + " results for " + target_genre

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_genre, category=category)

def search_by_track(target_track):
    header = ["Track Id", "Track Name", "Artist", "Album"]
    # Search for the track.

    tracks_by_track = services.get_tracks_by_track(target_track, repo.repo_instance)
    if len(tracks_by_track) == 0:
        return redirect(url_for('search_bp.not_found'))

    # number of tracks found by target_track
    table_name = str(len(tracks_by_track)) + " results for " + target_track

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_track)

@search_blueprint.route('/not_found', methods=['GET'])
def not_found():
    return render_template('tracks/not_found.html')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    search_type = SelectField('Search Type', choices=[('track', 'Track'), ('genre', 'Genre'), ('artist', 'Artist'), ('date', 'Date'), ('album', 'Album')])
    submit = SubmitField('Search')
