"""Initialize Flask app."""

from flask import Flask
from pathlib import Path



import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_object('config.Config')
    data_path = Path('music') / 'adapters' / 'data'

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)


    with app.app_context():
        from .tracks import tracks_browse
        app.register_blueprint(tracks_browse.tracks_blueprint)
        from .authentication import auth
        app.register_blueprint(auth.auth_blueprint)
        from .home import home
        app.register_blueprint(home.home_blueprint)
        from .tracks import search
        app.register_blueprint(search.search_blueprint)
        from .users import users
        app.register_blueprint(users.user_blueprint)
    return app
