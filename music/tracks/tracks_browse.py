from flask import Blueprint, render_template

# Setting up our blueprint
tracks_browse = Blueprint('tracks_browse', __name__, template_folder='templates')


@tracks_browse.route("/browse")
def table():
    header = ["Track Id", "Track Name", "Artist", "Length"]
    # Delete when we know how to get the data
    data = ["1", "Track 1", "Artist 1", "Length 1"]
    #return '<h1>Hey</h1>'
    return render_template('browse_tracks.html', headings = header, data = data)
