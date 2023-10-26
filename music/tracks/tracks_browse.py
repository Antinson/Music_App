from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from music.authentication.auth import login_required

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

import music.tracks.services as services
import music.adapters.repository as repo

# Setting up our blueprint
tracks_blueprint = Blueprint('tracks_bp', __name__, template_folder='templates')

@tracks_blueprint.route("/browse", methods=['GET'])
def get_tracks_table_view():
    return render_template('tracks/browse_tracks.html')


@tracks_blueprint.route("/browseRequest", methods=['GET', 'POST'])  # default page: browse all tracks in order of id
def browse_tracks():
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', type=int)

    start_index = (page - 1) * limit
    end_index = page * limit

    track_data_temp = services.get_all_track_ids(repo.repo_instance)
    track_data = track_data_temp[start_index:end_index]
    track_data_json = jsonify(services.get_tracks_by_id(track_data, repo.repo_instance))

    return track_data_json




# Individual track pages
@tracks_blueprint.route("/browse/<int:track_id>", methods=['GET', 'POST'])
def get_track_view(track_id):
    return 2


@tracks_blueprint.route("/totalTracks", methods=['GET'])  # default page: browse all tracks in order of id
def get_total_number_tracks():
    all_ids = services.get_all_track_ids(repo.repo_instance)
    total = len(all_ids)
    return str(total)

@tracks_blueprint.route("/track/<int:track_id>", methods=["GET", "POST"])
def get_individual_track_page(track_id):
    print(track_id)
    return render_template("tracks/track.html")

@tracks_blueprint.route("/getTrack/<int:track_id>", methods=["GET"])
def get_track_by_id(track_id):
    requested_track = services.get_track(track_id, repo.repo_instance)
    print("Request track is")
    print(requested_track)
    return jsonify(requested_track)



class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = 'Field must not contain profanity.'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review',
                           [DataRequired(), Length(min=4, message='Comment must be at least 4 characters long.'),
                            ProfanityFree(message='Your comment must not contain profanity.')])
    rating = SelectField('Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    submit = SubmitField('Submit')


class LikedForm(FlaskForm):
    liked = SubmitField('Liked')
