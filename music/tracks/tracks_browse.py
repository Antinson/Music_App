from flask import Blueprint, render_template, redirect, url_for
import music.tracks.services as services
import music.adapters.repository as repo

# Setting up our blueprint
tracks_blueprint = Blueprint('tracks_bp', __name__, template_folder='templates')


@tracks_blueprint.route("/browse")  # default page: browse all tracks in order of id
def get_tracks_table_view():
    header = ["Track Id", "Track Name", "Artist", "Length"]
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
    track = services.get_track(track_id, repo.repo_instance)
    return render_template('tracks/track.html', track=track, headings=header)
