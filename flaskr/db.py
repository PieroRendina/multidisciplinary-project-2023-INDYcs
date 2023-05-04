import bson

from flask import current_app, g
from werkzeug.local import LocalProxy
from flask_pymongo import PyMongo
import pprint
from pymongo.errors import DuplicateKeyError, OperationFailure
from bson.objectid import ObjectId
from bson.errors import InvalidId


def get_db():
    """
    Configuration method to return db instance
    """
    db = getattr(g, "_database", None)

    if db is None:
        db = g._database = PyMongo(current_app).db
    # return the database instance
    return db


# Use LocalProxy to read the global db instance with just `db`
db = LocalProxy(get_db)


def get_frame_bounding_boxes(movie_title, frame_id, fps=30):
    """
    Method to retrieve the bounding boxes associated to a frame in a movie
    :param movie_title: title of the movie whose frame is to retrieve
    :param frame_id: id of the frame to retrieve
    :return bounding_boxes: bounding boxes associated to the requested frame_id
    """
    detection_fps = get_detection_fps(movie_title)
    coeff = fps/detection_fps
    frame_id = int(frame_id/coeff)

    height, width = get_detection_shape(movie_title)

    movie_title = movie_title.replace("_", " ").lower()
    frame_info = db.movies_info.aggregate([{"$match": {"title": movie_title}},
                                            {"$project": {"frame": {"$arrayElemAt": ["$frames", frame_id]},
                                                          "_id": 0}}])
    frame_info = list(frame_info)
    # TODO: it's assuming that the frame exists and it will be the first to be returned
    bounding_boxes = frame_info[0]["frame"]["Coordinates"]
    items = frame_info[0]["frame"]["Items"]

    return bounding_boxes, items


def get_detection_fps(movie_title: str) -> int:
    """
    Method used to retrieve the fps used when running the detection algorithm
    :param movie_title: title of the movie whose detection fps is to retrieve
    :return detection_fps: fps used by the detection algorithm
    """
    documents = list(db.movies_info.find({"title": movie_title.replace("_", " ").lower()}, {"detection_fps": 1, "_id": 0}))
    assert len(documents) == 1
    return documents[0]["detection_fps"]


def get_detection_shape(movie_title: str) -> tuple:
    """
    Method to retrieve the size of the frames used when running the detection algorithm
    :param movie_title: title of the movie whose frame is to retrieve
    :return detection_shape: shape of the frames used for formerly running the detection algorithm
    """
    movie_title = movie_title.replace("_", " ").lower()

    height_doc = db.movies_info.aggregate([{"$match": {"title": movie_title}},
                                       {"$project": {"height": {"$arrayElemAt": ["$detection_size", 0]}}}])
    width_doc = db.movies_info.aggregate([{"$match": {"title": movie_title}},
                                      {"$project": {"width": {"$arrayElemAt": ["$detection_size", 1]}}}])
    height_doc = height_doc.next()
    width_doc = width_doc.next()
    height = height_doc["height"]
    width = width_doc["width"]
    detection_shape = (height, width)
    print(detection_shape)
    return detection_shape