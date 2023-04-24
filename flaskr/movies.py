from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response
)
import cv2
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


@bp.route('/show_movie', methods=["GET", "POST"])
def show_movie():
    def generate_movie_frames(title):
        # TODO change this according to the location of the file
        filepath = "flaskr"+title
        video_capture = cv2.VideoCapture(filepath)
        video_capture.set(cv2.CAP_PROP_FPS, 60)
        # Check if camera opened successfully
        if video_capture.isOpened() == False:
            print("Error opening video file")

        # Read until video is completed
        while video_capture.isOpened():
            success, frame = video_capture.read()  # read the camera frame
            if success:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

                # To adjust the frame rate and the speed of the video-player
                cv2.waitKey(25)

    if request.method == "POST":
        title = request.form['title']
        return Response(generate_movie_frames(title), mimetype='multipart/x-mixed-replace; boundary=frame')



