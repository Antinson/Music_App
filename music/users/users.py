from flask import Blueprint, render_template, redirect, url_for, flash, request
import music.users.services as services
import music.adapters.repository as repo

user_blueprint = Blueprint('user_bp', __name__, template_folder='templates')


@user_blueprint.route('/user/<user_id>', methods=['GET'])
def user(user_id):
    # Get the user's details.
    user = services.get_user(user_id, repo.repo_instance)
    if user is None:
        # No user to show, so return to the home page.
        return redirect(url_for('home_bp.home'))

    reviews = services.get_user_reviews(user_id, repo.repo_instance)
    liked_tracks = services.get_liked_tracks(user_id, repo.repo_instance)

    return render_template(
        'users/user.html',
        user=user,
        reviews=reviews,
        review_count=str(len(reviews)),
        liked_tracks=liked_tracks,
        liked_tracks_count=str(len(liked_tracks))
    )