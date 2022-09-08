from flask import Blueprint, render_template, redirect, url_for, flash, request
import music.tracks.services as services
import music.adapters.repository as repo



search_blueprint = Blueprint('search_bp', __name__, template_folder='templates')

# Tracks by Album
@search_blueprint.route("/search_by_album", methods=['GET', 'POST'])
def get_album_view():
    header = ["Album Id", "Title"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_album = request.form["nm"]
            if type(target_album) == int:
                return redirect(url_for('search_bp.get_tracks_by_album_id', target_album=target_album))
            else:
                return redirect(url_for('search_bp.get_tracks_by_album_str', target_album=target_album))
    except:
        return redirect(url_for('search_bp.not_found'))
    else:

        albums = services.get_albums(repo.repo_instance)
        return render_template('tracks/browse_albums.html', headings=header, albums=albums)


# when user types in str
@search_blueprint.route("/search_by_album/<target_album>", methods=['GET', 'POST'])
def get_tracks_by_album_str(target_album):
    header = ["Track Id", "Track Name", "Artist", "Album"]

    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_album = request.form["nm"]
            if type(target_album) == int:
                return redirect(url_for('search_bp.get_tracks_by_album_id', target_album=target_album))
            else:
                return redirect(url_for('search_bp.get_tracks_by_album_str', target_album=target_album))
    except:
        return redirect(url_for('search_bp.not_found'))

    # Get tracks that match album title
    tracks_by_album = services.get_tracks_by_album(target_album, repo.repo_instance)
    if len(tracks_by_album) == 0:
        return redirect(url_for('search_bp.not_found'))

    # number of tracks found by target_album
    table_name = str(len(tracks_by_album)) + " results for " + target_album

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_album)


# when user types in id
@search_blueprint.route("/search_by_album/<int:target_album>", methods=['GET', 'POST'])
def get_tracks_by_album_id(target_album):
    header = ["Track Id", "Track Name", "Artist", "Album"]

    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_album = request.form["nm"]
            if type(target_album) == int:
                return redirect(url_for('search_bp.get_tracks_by_album_id', target_album=target_album))
            else:
                return redirect(url_for('search_bp.get_tracks_by_album_str', target_album=target_album))
    except:
        return redirect(url_for('search_bp.not_found'))

    # Get tracks that match album id
    tracks_by_album = services.get_tracks_by_album(target_album, repo.repo_instance)

    # if no tracks found, redirect
    if len(tracks_by_album) == 0:
        return redirect(url_for('tracks_bp.not_found'))

    # get album title for display
    album_title = tracks_by_album[0]['album'].title

    # number of tracks found by target_album
    table_name = str(len(tracks_by_album)) + " results for " + album_title

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_album)


# Tracks by Artist
@search_blueprint.route("/search_by_artist", methods=['GET', 'POST'])
def get_tracks_by_artist_view():
    header = ["Artist Id", "Name"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_artist = request.form["nm"]
            if type(target_artist) == int:
                return redirect(url_for('search_bp.get_tracks_by_artist_id', target_artist=target_artist))
            else:
                return redirect(url_for('search_bp.get_tracks_by_artist_str', target_artist=target_artist))
    except:
        return redirect(url_for('search_bp.not_found'))
    else:
        artists = services.get_artists(repo.repo_instance)
        return render_template('tracks/browse_artists.html', headings=header, artists=artists)


# when user types in str
@search_blueprint.route("/search_by_artist/<target_artist>", methods=['GET', 'POST'])
def get_tracks_by_artist_str(target_artist):
    header = ["Track Id", "Track Name", "Artist", "Album"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_artist = request.form["nm"]
            if type(target_artist) == int:
                return redirect(url_for('search_bp.get_tracks_by_artist_id', target_artist=target_artist))
            else:
                return redirect(url_for('search_bp.get_tracks_by_artist_str', target_artist=target_artist))
    except:
        return redirect(url_for('search_bp.not_found'))

    # Get tracks that match artist name
    tracks_by_artist = services.get_tracks_by_artist(target_artist, repo.repo_instance)

    # if no tracks found, redirect
    if len(tracks_by_artist) == 0:
        return redirect(url_for('search_bp.not_found'))

    # number of tracks found by target_album
    table_name = str(len(tracks_by_artist)) + " results for " + target_artist

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_artist)

# when user types in id
@search_blueprint.route("/search_by_artist/<int:target_artist>", methods=['GET', 'POST'])
def get_tracks_by_artist_id(target_artist):
    header = ["Track Id", "Track Name", "Artist", "Album"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_artist = request.form["nm"]
            if type(target_artist) == int:
                return redirect(url_for('search_bp.get_tracks_by_artist_id', target_artist=target_artist))
            else:
                return redirect(url_for('search_bp.get_tracks_by_artist_str', target_artist=target_artist))
    except:
        return redirect(url_for('search_bp.not_found'))

    # Get tracks that match artist name
    tracks_by_artist = services.get_tracks_by_artist(target_artist, repo.repo_instance)

    # if no tracks found, redirect
    if len(tracks_by_artist) == 0:
        return redirect(url_for('search_bp.not_found'))


    # get artist name for display
    artist_name = tracks_by_artist[0]['artist'].full_name

    # number of tracks found by target_album
    table_name = str(len(tracks_by_artist)) + " results for " + artist_name

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_artist)
# Tracks by Genre
@search_blueprint.route("/search_by_genre", methods=['GET', 'POST'])
def get_genres_view():
    header = ['Genre Id', 'Title']
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_genre = request.form["nm"]
            if type(target_genre) == int:
                return redirect(url_for('search_bp.get_tracks_by_genre_id', target_genre=target_genre))
            else:
                return redirect(url_for('search_bp.get_tracks_by_genre_str', target_genre=target_genre))
    except:
        return redirect(url_for('search_bp.not_found'))
    else:
        genres = services.get_genres(repo.repo_instance)
        return render_template('tracks/browse_genres.html', headings=header, genres=genres)



# when user types in str
@search_blueprint.route("/search_by_genre/<target_genre>", methods=['GET', 'POST'])
def get_tracks_by_genre_str(target_genre):
    header = ["Track Id", "Track Name", "Artist", "Album"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_genre = request.form["nm"]
            if type(target_genre) == int:
                return redirect(url_for('search_bp.get_tracks_by_genre_id', target_genre=target_genre))
            else:
                return redirect(url_for('search_bp.get_tracks_by_genre_str', target_genre=target_genre))
    except:
        return redirect(url_for('search_bp.not_found'))

    # Get tracks that match artist name
    tracks_by_genre = services.get_tracks_by_genre(target_genre, repo.repo_instance)

    # if no tracks found, redirect
    if len(tracks_by_genre) == 0:
        return redirect(url_for('search_bp.not_found'))

    # number of tracks found by target_album
    table_name = str(len(tracks_by_genre)) + " results for " + target_genre

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_genre)



# when user types in id
@search_blueprint.route("/search_by_genre/<int:target_genre>", methods=['GET', 'POST'])
def get_tracks_by_genre_id(target_genre):
    header = ["Track Id", "Track Name", "Artist", "Album"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_genre = request.form["nm"]
            if type(target_genre) == int:
                return redirect(url_for('search_bp.get_tracks_by_genre_id', target_genre=target_genre))
            else:
                return redirect(url_for('search_bp.get_tracks_by_genre_str', target_genre=target_genre))
    except:
        return redirect(url_for('search_bp.not_found'))

    # Get tracks that match artist name
    tracks_by_genre = services.get_tracks_by_genre(target_genre, repo.repo_instance)

    # if no tracks found, redirect
    if len(tracks_by_genre) == 0:
        return redirect(url_for('search_bp.not_found'))

    # get genre name for display
    genre_name = tracks_by_genre[0]['track_genres'][0].name

    # number of tracks found by target_album
    table_name = str(len(tracks_by_genre)) + " results for " + genre_name

    return render_template('tracks/browse_tracks_by_category.html', headings=header, table_name=table_name, tracks=tracks_by_genre)

@search_blueprint.route("/search/not_found")
def not_found():
    return render_template('tracks/not_found.html')



# Tracks by date
@search_blueprint.route("/search_by_date", methods=['GET', 'POST'])
def get_tracks_by_date_view():
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_date = request.form["nm"]
            return redirect(url_for('search_bp.get_tracks_by_date', target_date=target_date))
    except:
        return redirect(url_for('search_bp.not_found'))
    return render_template('tracks/browse_tracks.html')


@search_blueprint.route("/search_by_date/<int:target_date>", methods=['GET', 'POST'])
def get_tracks_by_date(target_date):
    header = ["Track Id", "Track Name", "Artist", "Length"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_date = request.form["nm"]
            return redirect(url_for('search_bp.get_tracks_by_date', target_date=target_date))
    except:
        return redirect(url_for('search_bp.not_found'))

    # Get tracks with specified date, previous and next date of specified date
    tracks, prev_date, next_date = services.get_tracks_by_date(target_date, repo.repo_instance)
    prev_track_url = None
    next_track_url = None
    first_track_url = None
    last_track_url = None

    # number of tracks found by target_date
    table_name = str(len(tracks)) + " results for year " + str(target_date)

    # create links for previous and next buttons
    if prev_date is not None:
        prev_track_url = url_for('search_bp.get_tracks_by_date', target_date=prev_date)
    if next_date is not None:
        next_track_url = url_for('search_bp.get_tracks_by_date', target_date=next_date)

    return render_template('tracks/browse_tracks.html', headings=header,
                           tracks=tracks, prev_track_url=prev_track_url, next_track_url=next_track_url,
                           first_track_url=first_track_url, last_track_url=last_track_url, table_name=table_name)
