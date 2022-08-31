"""App entry point."""
from music import create_app
from music.tracks import tracks_browse

app = create_app()

if __name__ == "__main__":
    app.run(host='localhost', port=5001, threaded=False)