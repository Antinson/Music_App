from flask import Blueprint, render_template

# Setting up our blueprint
tracks_blueprint = Blueprint('tracks_browse', __name__, template_folder='templates')


@tracks_blueprint.route("/browse")
def table():
    header = ["Track Id", "Track Name", "Artist", "Length"]

    # data should be in the form of a list of tracks
    return "<p> working </p>"
    #return render_template('browse_tracks.html', headings = header, data = data)