from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
import music.users.services as services
import music.adapters.repository as repo

user_blueprint = Blueprint('user_bp', __name__, template_folder='templates')


# @user_blueprint.route('/user/<user_id>', methods=['GET'])
# def user(user_id):
#     # Get the user's details.
#     user = services.get_user(user_id, repo.repo_instance)
#     if user is None:
#         # No user to show, so return to the home page.
#         return redirect(url_for('home_bp.home'))

#     review_cursor = request.args.get('review_cursor')
#     lt_cursor = request.args.get('lt_cursor')

#     tracks_per_page = 5
#     reviews_per_page = 2

#     if review_cursor is None:
#         review_cursor = 0
#     else:
#         review_cursor = int(float(review_cursor))

#     if lt_cursor is None:
#         lt_cursor = 0
#     else:
#         lt_cursor = int(float(lt_cursor))

#     # get reviews and liked tracks
#     reviews = services.get_user_reviews(user_id, repo.repo_instance)
#     liked_tracks = services.get_liked_tracks(user_id, repo.repo_instance)

#     reviews_sliced = reviews[review_cursor:review_cursor + reviews_per_page]
#     liked_tracks_sliced = liked_tracks[lt_cursor:lt_cursor + tracks_per_page]

#     review_first_page_url = None
#     review_next_page_url = None
#     review_prev_page_url = None
#     review_last_page_url = None

#     if review_cursor > 0:
#         # there is a previous page
#         if review_cursor - reviews_per_page > 0:
#             review_prev_page_url = url_for('user_bp.user', user_id=user_id,
#                                            review_cursor=review_cursor - reviews_per_page)
#         else:
#             review_prev_page_url = url_for('user_bp.user', user_id=user_id)
#         review_first_page_url = url_for('user_bp.user', user_id=user_id)

#     if review_cursor + reviews_per_page < len(reviews):
#         # there is a following page
#         review_next_page_url = url_for('user_bp.user', user_id=user_id, review_cursor=review_cursor + reviews_per_page)
#         last_cursor = int(float(len(reviews) / reviews_per_page))
#         review_last_page_url = url_for('user_bp.user', user_id=user_id, review_cursor=last_cursor * reviews_per_page)

#     # lt for liked tracks
#     lt_first_page_url = None
#     lt_next_page_url = None
#     lt_prev_page_url = None
#     lt_last_page_url = None

#     if lt_cursor > 0:
#         # there is a previous page
#         if lt_cursor - tracks_per_page > 0:
#             lt_prev_page_url = url_for('user_bp.user', user_id=user_id,
#                                            lt_cursor=lt_cursor - tracks_per_page)
#         else:
#             lt_prev_page_url = url_for('user_bp.user', user_id=user_id)
#         lt_first_page_url = url_for('user_bp.user', user_id=user_id)

#     if lt_cursor + tracks_per_page < len(liked_tracks):
#         # there is a following page
#         lt_next_page_url = url_for('user_bp.user', user_id=user_id, lt_cursor=lt_cursor + tracks_per_page)
#         last_cursor = int(float(len(liked_tracks) / tracks_per_page))
#         lt_last_page_url = url_for('user_bp.user', user_id=user_id, lt_cursor=last_cursor * tracks_per_page)

#     return render_template(
#         'users/user.html',
#         user=user,
#         reviews=reviews_sliced,
#         review_count=str(len(reviews)),
#         liked_tracks=liked_tracks_sliced,
#         liked_tracks_count=str(len(liked_tracks)),
#         review_prev_page_url=review_prev_page_url,
#         review_first_page_url=review_first_page_url,
#         review_next_page_url=review_next_page_url,
#         review_last_page_url=review_last_page_url,
#         lt_first_page_url=lt_first_page_url,
#         lt_next_page_url=lt_next_page_url,
#         lt_prev_page_url=lt_prev_page_url,
#         lt_last_page_url=lt_last_page_url
#     )



@user_blueprint.route('/user/<user_name>', methods=['GET'])
def user_api(user_name):
    return render_template('users/user.html', user_name=user_name)
    

@user_blueprint.route('/getLikedTracks/<user_name>', methods=['GET'])
def get_liked_tracks(user_name):
    liked_tracks = services.get_liked_tracks(str(user_name).lower(), repo.repo_instance)
    return jsonify(liked_tracks)

@user_blueprint.route('/getReviews/<user_name>', methods=['GET'])
def get_user_reviews(user_name):
    user_reviews = services.get_user_reviews(str(user_name).lower(), repo.repo_instance)
    return jsonify(user_reviews)


