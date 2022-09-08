from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash, request
import music.tracks.services as services
import music.adapters.repository as repo

# Setting up our blueprint
tracks_blueprint = Blueprint('tracks_bp', __name__, template_folder='templates')


@tracks_blueprint.route("/browse", methods=['GET', 'POST'])  # default page: browse all tracks in order of id
def get_tracks_table_view():
    header = ["Track Id", "Track Name", "Artist", "Length"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            track_id = request.form["nm"]
            # Redirect user to track
            return redirect(url_for('tracks_bp.get_track_view', track_id=track_id))
    except:
        # If the user has entered an invalid track id or None, redirect to not found
        return redirect(url_for('tracks_bp.not_found'))


    else:
        tracks = services.get_all_tracks(repo.repo_instance)

        return render_template('tracks/browse_tracks.html',
                               headings=header,
                               tracks=tracks)


# Individual track pages
@tracks_blueprint.route("/browse/<int:track_id>")
def get_track_view(track_id):
    header = ["Track Id", "Track Name", "Artist", "Length", "URL"]
    # Grabbing data from our memory repo through our services layer
    try:
        track = services.get_track(track_id, repo.repo_instance)
    except:
        return redirect(url_for('tracks_bp.not_found', track_id=track_id))
    return render_template('tracks/track.html', track=track, headings=header)


@tracks_blueprint.route("/browse/not_found")
def not_found():
    return render_template('tracks/not_found.html')


# Tracks by date
@tracks_blueprint.route("/search_by_date", methods=['GET', 'POST'])
def get_tracks_by_date_view():
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_date = request.form["nm"]
            return redirect(url_for('tracks_bp.get_tracks_by_date', target_date=target_date))
    except:
        return redirect(url_for('tracks_bp.not_found'))
    return render_template('tracks/browse_tracks.html')


@tracks_blueprint.route("/search_by_date/<int:target_date>", methods=['GET', 'POST'])
def get_tracks_by_date(target_date):
    header = ["Track Id", "Track Name", "Artist", "Length"]
    try:
        # See if user has put anything in search box and pressed submit
        if request.method == 'POST':
            # Get the search term from the form
            target_date = request.form["nm"]
            return redirect(url_for('tracks_bp.get_tracks_by_date', target_date=target_date))
    except:
        return redirect(url_for('tracks_bp.not_found'))

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
        prev_track_url = url_for('tracks_bp.get_tracks_by_date', target_date=prev_date)
    if next_date is not None:
        next_track_url = url_for('tracks_bp.get_tracks_by_date', target_date=next_date)

    return render_template('tracks/browse_tracks.html', headings=header,
                           tracks=tracks, prev_track_url=prev_track_url, next_track_url=next_track_url,
                           first_track_url=first_track_url, last_track_url=last_track_url, table_name=table_name)
