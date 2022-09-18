
from datetime import date

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from music.authentication.auth import login_required

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError



import music.tracks.services as services
import music.adapters.repository as repo

# Setting up our blueprint
tracks_blueprint = Blueprint('tracks_bp', __name__, template_folder='templates')


@tracks_blueprint.route("/browse", methods=['GET', 'POST'])  # default page: browse all tracks in order of id
def get_tracks_table_view():
    header = ["Track Id", "Track Name", "Artist", "Length"]
    tracks_per_page = 19
    cursor = request.args.get('cursor')
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


        if cursor is None:
            cursor = 0
        else:
            cursor = int(float(cursor))

        track_ids = services.get_all_track_ids(repo.repo_instance)
        tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)

        first_page_url = None
        prev_page_url = None
        next_page_url = None
        last_page_url = None

        if cursor > 0:
            # there are previous pages
            if cursor - tracks_per_page < 0:
                prev_page_url = url_for('tracks_bp.get_tracks_table_view')
            else:
                prev_page_url = url_for('tracks_bp.get_tracks_table_view', cursor=cursor - tracks_per_page)
            first_page_url = url_for('tracks_bp.get_tracks_table_view')

        if cursor + tracks_per_page < len(track_ids):
            # there are more pages
            next_page_url = url_for('tracks_bp.get_tracks_table_view', cursor=cursor +tracks_per_page)
            last_page_url = url_for('tracks_bp.get_tracks_table_view', cursor=int(len(track_ids)) - tracks_per_page)

        return render_template(
            'tracks/browse_tracks.html',
            headings=header,
            tracks=tracks,
            first_page_url=first_page_url,
            prev_page_url=prev_page_url,
            next_page_url=next_page_url,
            last_page_url=last_page_url)


# Individual track pages
@tracks_blueprint.route("/browse/<int:track_id>", methods=['GET', 'POST'])
def get_track_view(track_id):
    header = ["Track Id", "Track Name", "Artist", "Length", "URL"]
    form = ReviewForm()
    liked = LikedForm()
    reviews = services.get_reviews_for_track(track_id, repo.repo_instance)
    logged_in = False
    track_already_liked = None
    # Grabbing data from our memory repo through our services layer
    try:
        track = services.get_track(track_id, repo.repo_instance)
    except:
        return redirect(url_for('tracks_bp.not_found', track_id=track_id))

    try:
        user_name = session['user_name']
        logged_in = True
        user_liked_tracks = services.get_user_liked_tracks(user_name.lower(), repo.repo_instance)
        if track in user_liked_tracks:
            track_already_liked = True
        else:
            track_already_liked = False
    except:
        pass

    if request.method == 'POST':
        try:
            if request.form.get('liked') != None:
                services.add_track_to_user(user_name, track_id, repo.repo_instance)
                track_already_liked = True

                return render_template('tracks/track.html', track=track, headings=header, form=form, reviews=reviews, logged_in = logged_in, track_already_liked=track_already_liked)
            elif request.form.get('unliked') != None:
                services.remove_track_from_user(user_name, track_id, repo.repo_instance)
                track_already_liked = False

                return render_template('tracks/track.html', track=track, headings=header, form=form, reviews=reviews, logged_in = logged_in, track_already_liked=track_already_liked)

            elif form.validate_on_submit():
            # Storing the new comment
                services.add_review(track_id, form.review.data, user_name, int(form.rating.data), repo.repo_instance)
                # Redirect to the track page
                return redirect(url_for('tracks_bp.get_track_view', track_id=track_id))
        except:
            return redirect(url_for('auth_bp.login'))

    if request.method == 'GET':
        pass

    return render_template('tracks/track.html', track=track, headings=header, form=form, reviews=reviews, logged_in = logged_in, track_already_liked = track_already_liked)


@tracks_blueprint.route("/browse/not_found")
def not_found():
    return render_template('tracks/not_found.html')





class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = 'Field must not contain profanity.'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)

class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [DataRequired(), Length(min=4, message='Comment must be at least 4 characters long.'),
                                        ProfanityFree(message = 'Your comment must not contain profanity.')])
    rating = SelectField('Rating', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])
    submit = SubmitField('Submit')


class LikedForm(FlaskForm):
    liked = SubmitField('Liked')
