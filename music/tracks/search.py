from flask import Blueprint, render_template, redirect, url_for, flash, request
import music.tracks.services as services
import music.adapters.repository as repo

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

search_blueprint = Blueprint('search_bp', __name__, template_folder='templates')


@search_blueprint.route('/search/<target_genre>', methods=['GET', 'POST'])
@search_blueprint.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if request.method == 'POST':
        return search_by(search_form)

    terms_per_page = 10
    cursor = request.args.get('cursor')


    if cursor is None:
        cursor = 0
    else:
        cursor = int(float(cursor))

    track_ids = services.get_all_track_ids(repo.repo_instance)
    tracks = services.get_tracks_by_id(track_ids, repo.repo_instance)

    # get what to view
    view_target = request.args.get('view_target')
    if view_target is None:
        # if none set default to release year
        view_target = 'Release Years'


    terms = []

    # get terms according to selected view_target
    if view_target == 'Artists':
        for track in tracks:
            if track['artist'] is not None and track['artist'].full_name not in terms:
                terms.append(track['artist'].full_name)
                terms.sort()
    if view_target == 'Albums':
        for track in tracks:
            if track['album']is not None and track['album'].title not in terms:
                terms.append(track['album'].title)
                terms.sort()
    if view_target == 'Genres':
        for track in tracks:
            for genre in track['track_genres']:
                if genre.name not in terms:
                    terms.append(genre.name)
                    terms.sort()
    if view_target == 'Release Years':
        terms = services.get_all_dates(repo.repo_instance)

    # slice the terms accordingly, this limits the amount of terms to show
    sliced_terms = terms[cursor:cursor + terms_per_page]


    # set up nav links
    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:
        # there are previous pages
        if cursor - terms_per_page < 0:
            prev_page_url = url_for('search_bp.search', view_target=view_target)
        else:
            prev_page_url = url_for('search_bp.search', view_target=view_target, cursor=cursor - terms_per_page)
        first_page_url = url_for('search_bp.search', view_target=view_target)

    if cursor + terms_per_page < len(terms):
        # there are more pages
        next_page_url = url_for('search_bp.search', view_target=view_target, cursor=cursor + terms_per_page)
        last_page_url = url_for('search_bp.search', view_target=view_target,
                                cursor=len(terms) - terms_per_page)

    # For a GET request, return the search page.
    return render_template(
        'tracks/search.html',
        title='Search',
        form=search_form,
        search_target=url_for('search_bp.search'),
        sliced_terms=sliced_terms,
        first_page_url=first_page_url,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        last_page_url=last_page_url,
        target_view=view_target
    )


def search_by(form):
    if form.search_type.data == 'track':
        return redirect(url_for('search_bp.search_by_track', target_track=form.search.data))
    elif form.search_type.data == 'genre':
        return redirect(url_for('search_bp.search_by_genre', target_genre=form.search.data))
    elif form.search_type.data == 'artist':
        return redirect(url_for('search_bp.search_by_artist', target_artist=form.search.data))
    elif form.search_type.data == 'release year':
        return redirect(url_for('search_bp.search_by_date', target_date=form.search.data))
    elif form.search_type.data == 'album':
        return redirect(url_for('search_bp.search_by_album', target_album=form.search.data))


@search_blueprint.route('/search_by_album', methods=['GET'])
def search_by_album():
    header = ["Track Id", "Track Title", "Artist", "Album", "Length"]
    category = "album"
    tracks_per_page = 15

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
        if len(track_ids) == 0:
            raise ValueError
        # Limiting tracks to display
        tracks_by_album = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)
    except ValueError:
        return redirect(url_for('search_bp.not_found', target_search=target_album, term='Album'))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:
        # There is a previous page
        if cursor - tracks_per_page > 0:
            prev_page_url = url_for('search_bp.search_by_album', target_album=target_album,
                                    cursor=cursor - tracks_per_page)
        else:
            prev_page_url = url_for('search_bp.search_by_album', target_album=target_album)
        first_page_url = url_for('search_bp.search_by_album', target_album=target_album)
    if cursor + tracks_per_page < len(track_ids):
        # There is a following page
        next_page_url = url_for('search_bp.search_by_album', target_album=target_album, cursor=cursor + tracks_per_page)
        last_cursor = int(float(len(track_ids) / tracks_per_page))
        last_page_url = url_for('search_bp.search_by_album', target_album=target_album,
                                cursor=last_cursor * tracks_per_page)

    # Number of tracks found by target_album
    table_name = "Search by Album: " + str(len(track_ids)) + " results for '" + target_album + "'"

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
    header = ["Track Id", "Track Title", "Artist", "Album", "Length"]
    category = "artist"
    tracks_per_page = 15

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
        if len(track_ids) == 0:
            raise ValueError
        # Limiting tracks to display
        tracks_by_artist = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)
    except ValueError:
        return redirect(url_for('search_bp.not_found', target_search=target_artist, term='Artist'))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:
        # There is a previous page
        if cursor - tracks_per_page > 0:
            prev_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist,
                                    cursor=cursor - tracks_per_page)
        else:
            prev_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist)
        first_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist)
    if cursor + tracks_per_page < len(track_ids):
        # There is a following page
        next_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist,
                                cursor=cursor + tracks_per_page)
        last_cursor = int(float(len(track_ids) / tracks_per_page))
        last_page_url = url_for('search_bp.search_by_artist', target_artist=target_artist,
                                cursor=last_cursor * tracks_per_page)

    # Number of tracks found by target_artist
    table_name = "Search by Artist: " + str(len(track_ids)) + " results for '" + target_artist + "'"

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
    header = ["Track Id", "Track Title", "Artist", "Album", "Length"]
    category = "date"
    tracks_per_page = 15

    # Get parameters
    target_date = request.args.get('target_date')
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(float(cursor))

    # Search for the date.
    try:
        # Get all tracks by specified date (list), and get prev and next dates (int)
        track_ids, prev_date, next_date = services.get_track_ids_by_date(int(target_date), repo.repo_instance)
        if len(track_ids) == 0:
            raise ValueError
        # Limiting tracks to display
        tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)

    except ValueError:
        return redirect(url_for('search_bp.not_found', target_search=target_date, term='Release Year'))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    prev_year_url = None
    next_year_url = None

    if cursor > 0:
        # There is a previous page
        if cursor - tracks_per_page > 0:
            prev_page_url = url_for('search_bp.search_by_date', target_date=target_date,
                                    cursor=cursor - tracks_per_page)
        else:
            prev_page_url = url_for('search_bp.search_by_date', target_date=target_date)

        first_page_url = url_for('search_bp.search_by_date', target_date=target_date)

    if cursor + tracks_per_page < len(track_ids):
        # There is a following page
        next_page_url = url_for('search_bp.search_by_date', target_date=target_date, cursor=cursor + tracks_per_page)
        last_cursor = int(float(len(track_ids) / tracks_per_page))
        last_page_url = url_for('search_bp.search_by_date', target_date=target_date,
                                cursor=last_cursor * tracks_per_page)

    if prev_date is not None:
        prev_year_url = url_for('search_bp.search_by_date', target_date=prev_date)
    if next_date is not None:
        next_year_url = url_for('search_bp.search_by_date', target_date=next_date)

    # number of tracks found by target_date
    table_name = "Search by Release Year: " + str(len(track_ids)) + " results for '" + target_date + "'"

    return render_template(
        'tracks/browse_tracks_by_category.html',
        headings=header,
        table_name=table_name,
        tracks=tracks,
        category=category,
        first_page_url=first_page_url,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        last_page_url=last_page_url,
        prev_year_url=prev_year_url,
        next_year_url=next_year_url)


@search_blueprint.route('/search_by_genre', methods=['GET'])
def search_by_genre():
    header = ["Track Id", "Track Title", "Artist", "Album", "Genre/s"]
    category = "genre"
    tracks_per_page = 10

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
        if len(track_ids) == 0:
            raise ValueError
        tracks_by_genre = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)
    except ValueError:
        return redirect(url_for('search_bp.not_found', target_search=target_genre, term='Genre'))

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
        last_page_url = url_for('search_bp.search_by_genre', target_genre=target_genre,
                                cursor=last_cursor * tracks_per_page)

    # Number of tracks found by target_genre
    table_name = "Search by Genre: " + str(len(track_ids)) + " results for '" + target_genre + "'"

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


@search_blueprint.route('/search_by_track', methods=['GET'])
def search_by_track():
    header = ["Track Id", "Track Title", "Artist", "Album", "Length"]
    category = "track"
    tracks_per_page = 15

    # Get parameters
    target_track = request.args.get('target_track')
    cursor = request.args.get('cursor')

    if cursor is None:
        cursor = 0
    else:
        cursor = int(float(cursor))

    try:
        # Get all tracks of specified track title
        track_ids = services.get_track_ids_by_track_title(target_track, repo.repo_instance)
        if len(track_ids) == 0:
            raise ValueError
        # Limiting tracks to display
        tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)
    except ValueError:
        return redirect(url_for('search_bp.not_found', target_search=target_track, term='Track Title'))

    first_page_url = None
    prev_page_url = None
    next_page_url = None
    last_page_url = None

    if cursor > 0:
        # There is a previous page
        if cursor - tracks_per_page > 0:
            prev_page_url = url_for('search_bp.search_by_track', target_track=target_track,
                                    cursor=cursor - tracks_per_page)
        else:
            prev_page_url = url_for('search_bp.search_by_track', target_track=target_track)

        first_page_url = url_for('search_bp.search_by_track', target_track=target_track)

    if cursor + tracks_per_page < len(track_ids):
        # There is a following page
        next_page_url = url_for('search_bp.search_by_track', target_track=target_track, cursor=cursor + tracks_per_page)
        last_cursor = int(float(len(track_ids) / tracks_per_page))
        last_page_url = url_for('search_bp.search_by_track', target_track=target_track,
                                cursor=last_cursor * tracks_per_page)

    # Number of tracks found by target_track
    table_name = "Search by Track Title: " + str(len(track_ids)) + " results for '" + target_track + "'"

    return render_template(
        'tracks/browse_tracks_by_category.html',
        headings=header,
        table_name=table_name,
        tracks=tracks,
        category=category,
        first_page_url=first_page_url,
        prev_page_url=prev_page_url,
        next_page_url=next_page_url,
        last_page_url=last_page_url)


@search_blueprint.route('/not_found', methods=['GET'])
def not_found():
    target_search = request.args.get('target_search')
    term = request.args.get('term')
    return render_template('tracks/not_found.html', target_search=target_search, term=term)


class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    search_type = SelectField('Search Type',
                              choices=[('track', 'Track'), ('genre', 'Genre'), ('artist', 'Artist'), ('release year', 'Release Year'),
                                       ('album', 'Album')])
    submit = SubmitField('Search')
