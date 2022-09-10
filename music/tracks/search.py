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
    if form.search_type.data == 'track':
        return search_by_track(form.search.data)
    elif form.search_type.data == 'genre':
        return redirect(url_for('search_bp.search_by_genre', target_genre=form.search.data))
    elif form.search_type.data == 'artist':
        return redirect(url_for('search_bp.search_by_artist', target_artist=form.search.data))
    elif form.search_type.data == 'date':
        return redirect(url_for('search_bp.search_by_date', target_date=form.search.data))
    elif form.search_type.data == 'album':
        return redirect(url_for('search_bp.search_by_album', target_album=form.search.data))

@search_blueprint.route('/search_by_album', methods=['GET'])
def search_by_album():
    header = ["Track Id", "Track Name", "Artist", "Album"]
    category = "album"
    tracks_per_page = 19

    # Get parameters
    target_album = request.args.get('target_album')
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(float(cursor))

    # Search for the album.
    try:
        # Get all tracks by specified album
        track_ids = services.get_track_ids_by_album(target_album, repo.repo_instance)
        tracks_by_album = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)
    except ValueError:
        return redirect(url_for('search_bp.not_found'))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:
        # There is a previous page
        if cursor - tracks_per_page > 0:
            prev_page_url = url_for('search_bp.search_by_album', target_album=target_album, cursor=cursor - tracks_per_page)
        else:
            prev_page_url = url_for('search_bp.search_by_album', target_album=target_album)
        first_page_url = url_for('search_bp.search_by_album', target_album=target_album)
    if cursor + tracks_per_page < len(track_ids):
        # There is a following page
        next_page_url = url_for('search_bp.search_by_album', target_album=target_album, cursor=cursor + tracks_per_page)
        last_cursor = int(float(len(track_ids) / tracks_per_page))
        last_page_url = url_for('search_bp.search_by_album', target_album=target_album, cursor=last_cursor * tracks_per_page)


    # Number of tracks found by target_album
    table_name = str(len(track_ids)) + " results for " + target_album

    return render_template(
        'tracks/browse_tracks_by_category.html',
        headings=header,
        table_name=table_name,
        tracks=tracks_by_album,
        category=category,
        first_page_url=first_page_url,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        last_page_url=last_page_url)
@search_blueprint.route('/search_by_artist', methods=['GET'])
def search_by_artist():
    header = ["Track Id", "Track Name", "Artist", "Album"]
    category = "artist"
    tracks_per_page = 19

    # Get parameters
    target_artist = request.args.get('target_artist')
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(float(cursor))

    # Search for the artist.
    try:
        # Get all tracks by specified artist
        track_ids = services.get_track_ids_by_artist(target_artist, repo.repo_instance)
        # Limiting tracks to display
        tracks_by_artist = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)
    except ValueError:
        return redirect(url_for('search_bp.not_found'))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:
        # There is a previous page
        if cursor - tracks_per_page > 0:
            prev_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist, cursor=cursor - tracks_per_page)
        else:
            prev_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist)
        first_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist)
    if cursor + tracks_per_page < len(track_ids):
        # There is a following page
        next_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist, cursor=cursor + tracks_per_page)
        last_cursor = int(float(len(track_ids) / tracks_per_page))
        last_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist, cursor=last_cursor * tracks_per_page)


    # Number of tracks found by target_artist
    table_name = str(len(track_ids)) + " results for " + target_artist

    return render_template(
        'tracks/browse_tracks_by_category.html',
        headings=header,
        table_name=table_name,
        tracks=tracks_by_artist,
        category=category,
        first_page_url=first_page_url,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        last_page_url=last_page_url)

@search_blueprint.route('/search_by_date', methods=['GET'])
def search_by_date():
    header = ["Track Id", "Track Name", "Artist", "Length"]
    category = "date"
    tracks_per_page = 19

    # Get parameters
    target_date = request.args.get('target_date')
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(float(cursor))

    # Search for the date.
    try:
        # Get all tracks by the specified date
        track_ids, prev_year, next_year = services.get_track_ids_by_date(target_date, repo.repo_instance)
        # Limiting tracks to display
        tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)

    except ValueError:
        return redirect(url_for('search_bp.not_found'))


    prev_year_url = None
    first_page_url = None
    prev_page_url = None

    next_year_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:
        # There is a previous page
        if cursor - tracks_per_page < 0:
            prev_page_url = url_for('search_bp.search_by_date', target_date=target_date, cursor=cursor - tracks_per_page)
        else:
            prev_page_url = url_for('search_bp.search_by_date', target_date=target_date)
        first_page_url = url_for('search_bp.search_by_date', target_date=target_date)
    if cursor + tracks_per_page < len(track_ids):
        # There is a following page
        next_page_url = url_for('search_bp.search_by_date', target_date=target_date, cursor=cursor + tracks_per_page)

        last_cursor = int(len(track_ids))
        if len(track_ids) % tracks_per_page == 0:
            last_cursor -= tracks_per_page
        last_page_url = url_for('search_bp.search_by_date', target_date=target_date, cursor=last_cursor)

    if prev_year is not None:
        # There is a previous year
        prev_year_url = url_for('search_bp.search_by_date', target_date=prev_year)
    if next_year is not None:
        # There is a following year
        next_year_url = url_for('search_bp.search_by_date', target_date=next_year)


    # Number of tracks found by target_date
    table_name = str(len(tracks)) + " results for year " + str(target_date)

    return render_template(
        'tracks/browse_tracks_by_category.html',
        headings=header,
        table_name=table_name,
        tracks=track_ids,
        category=category,
        prev_year_url=prev_year_url,
        next_year_url=next_year_url,
        first_page_url=first_page_url,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        last_page_url=last_page_url)

@search_blueprint.route('/search_by_genre', methods=['GET'])
def search_by_genre():
    header = header = ["Track Id", "Track Name", "Artist", "Album", "Genre Id"]
    category = "genre"
    tracks_per_page = 19

    # Get parameters
    target_genre = request.args.get('target_genre')
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(float(cursor))

    # Search for the genre.
    try:
        track_ids = services.get_track_ids_by_genre(target_genre, repo.repo_instance)
        tracks_by_genre = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)
    except ValueError:
        return redirect(url_for('search_bp.not_found'))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:
        # There is a previous page
        if cursor - tracks_per_page > 0:
            prev_page_url = url_for('search_bp.search_by_genre', target_genre=target_genre,
                                    cursor=cursor - tracks_per_page)
        else:
            prev_page_url = url_for('search_bp.search_by_genre', target_genre=target_genre)

        first_page_url = url_for('search_bp.search_by_genre', target_genre=target_genre)

    if cursor + tracks_per_page < len(track_ids):
        # There is a following page
        next_page_url = url_for('search_bp.search_by_genre', target_genre=target_genre, cursor=cursor + tracks_per_page)
        last_cursor = int(float(len(track_ids) / tracks_per_page))
        last_page_url = url_for('search_bp.search_by_genre', target_genre=target_genre, cursor=last_cursor * tracks_per_page)

    # Number of tracks found by target_genre
    table_name = str(len(track_ids)) + " results for " + target_genre

    return render_template(
        'tracks/browse_tracks_by_category.html',
        headings=header,
        table_name=table_name,
        tracks=tracks_by_genre,
        category=category,
        first_page_url=first_page_url,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        last_page_url=last_page_url)


def search_by_track(target_track):
    header = ["Track Id", "Track Name", "Artist", "Album"]
    # Search for the track.

    tracks_by_track = services.get_tracks_by_track(target_track, repo.repo_instance)
    if len(tracks_by_track) == 0:
        return redirect(url_for('search_bp.not_found'))

    # Number of tracks found by target_track
    table_name = str(len(tracks_by_track)) + " results for " + target_track

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name,
                           tracks=tracks_by_track)

@search_blueprint.route('/not_found', methods=['GET'])
def not_found():
    return render_template('tracks/not_found.html')

class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    search_type = SelectField('Search Type', choices=[('track', 'Track'), ('genre', 'Genre'), ('artist', 'Artist'), ('date', 'Date'), ('album', 'Album')])
    submit = SubmitField('Search')
