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
        return redirect(url_for('tracks_bp.not_found', track_id=track_id))
    

    else:
        tracks = services.get_all_tracks(repo.repo_instance)



        # work in progress
        # function: limits the number of tracks displayed and sets the urls appropriately

        tracks_per_page = 45
        tracks_on_page = 0

        first_track_url = None
        last_track_url = None
        next_track_url = None
        prev_track_url = None

        if tracks_on_page > 0:
            # there are previous tracks
            prev_track_url = url_for('tracks_bp.get_tracks_table_view')
            first_track_url = url_for('tracks_bp.get_tracks_table_view')
        



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


@tracks_blueprint.route("/browse/<int:track_id>/not_found")
def not_found(track_id):
    return render_template('tracks/not_found.html', track_id=track_id)