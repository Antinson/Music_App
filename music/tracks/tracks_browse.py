from flask import Blueprint, render_template

tracks_browse = Blueprint('tracks_browse', __name__, static_folder='static', template_folder='templates', url_prefix='/tracks')

headings = ("Track_ID", "Track_Name", "Artist_Name","Track_Length")

@tracks_browse.route("/browse")

def table():
    return render_template('tracks_browse.html')


