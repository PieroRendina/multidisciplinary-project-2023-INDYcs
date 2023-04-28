import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
import cv2
from ffpyplayer.player import MediaPlayer
from werkzeug.exceptions import abort
# from flaskr.auth import login_required
# from flaskr.db import get_db

bp = Blueprint('movies', __name__)


@bp.route('/', methods=["GET", "POST"])
def index():
    """
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    """
    movies = [{"title": "Inception"}, {"title": "Avengers_Age_of_Ultron"}]
    return render_template('movies/index.html', movies=movies)


@bp.route('/select_movie', methods=["GET", "POST"])
def select_movie():
    if request.method == "POST":
        global title
        title = request.form['title']
        return render_template('movies/show_movie.html', title=title)


@bp.route('/show_movie')
def show_movie():
    return Response(generate_movie_frames(title), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_movie_frames(title):
    # TODO change this according to the location of the file
    filepath = "flaskr" + title
    video_capture = cv2.VideoCapture(filepath)
    audio_capture = MediaPlayer(filepath)
    # Check if camera opened successfully
    if not video_capture.isOpened():
        print("Error opening video file")
        # Read until video is completed
    while video_capture.isOpened():
        success, frame = video_capture.read()  # read the camera frame
        audio_frame, val = audio_capture.get_frame()
        if success:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # To play the audio
            if val != 'eof' and audio_frame is not None:
            # audio
                img, t = audio_frame
            yield (b'--frame\r\n' 
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            # To adjust the frame rate and the speed of the video-player
            cv2.waitKey(25)


