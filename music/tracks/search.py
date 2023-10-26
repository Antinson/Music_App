from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, json
import music.tracks.services as services
import music.adapters.repository as repo

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

search_blueprint = Blueprint('search_bp', __name__, template_folder='templates')


@search_blueprint.route('/search', methods=['GET'])
def searchget():
    return render_template('tracks/search.html')

@search_blueprint.route('/search', methods=['POST'])
def search():
    try:
        json_data = request.json
        ids = services.get_all_track_ids(repo.repo_instance)
        result = get_tracks(ids)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

@search_blueprint.route('/getCards', methods=['GET'])
def searchgets():
    try:
        ids = services.get_all_track_ids(repo.repo_instance)
        print(ids)
        result = services.get_tracks_by_id([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], repo.repo_instance)
        print(result)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}) 

# def search():
#     try:
#         json_data = request.json
#         category = json_data.get("category")
#         data = json_data.get("data")
        
#         categoryoptions = {
#             "id": services.get_track,
#             "date": services.get_track_ids_by_date,
#             "title": services.get_track_ids_by_track_title,
#             "album": services.get_track_ids_by_album,
#             "artist": services.get_track_ids_by_artist,
#             "genre": services.get_track_ids_by_genre,
#         }

#         if category in categoryoptions:
#             result = categoryoptions[category](data, repo.repo_instance)
#             print(get_tracks(result))
#             return jsonify(get_tracks(result))
#         else:
#             return jsonify({"error": "Invalid category"})
#     except Exception as e:
#         return jsonify({"error": str(e)})


def get_tracks(ids):
    return services.get_tracks_by_id(ids, repo.repo_instance)
