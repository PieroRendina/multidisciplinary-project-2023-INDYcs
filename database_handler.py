import pymongo
from urllib.parse import quote_plus


def db_connection(username: str, password: str) -> pymongo.MongoClient:
    """
    Method to instantiate a connection to a MongoDB Atlas instance
    :param username: username to access the database
    :param password: password to access the database
    :return client: a client connected to the database instance
    """
    uri = get_db_uri(username, password)
    client = pymongo.MongoClient(uri)
    return client


def get_db_uri(username: str, password: str) -> str:
    """
    Method to retrieve the connection URI for a MongoDB Atlas instance
    :param username: username to access the database
    :param password: password to access the database
    :return client: a client connected to the database instance
    """
    username = quote_plus(username)
    password = quote_plus(password)
    cluster = 'cluster0.hns6k.mongodb.net'
    options = '?ssl=true&tlsAllowInvalidCertificates=true'
    uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + "/movies" + options
    return uri


def get_frame_bounding_boxes(collection, movie_title, frame_id):
    """
    Method to retrieve the bounding boxes associated to a frame in a movie
    :param collection: MongoDB collection which stores a document for each movie with its own array of frames
    :param movie_title: title of the movie whose frame is to retrieve
    :param frame_id: id of the frame to retrieve
    :return bounding_boxes: bounding boxes associated to the requested frame_id
    """
    frame_info = collection.aggregate([{"$match": {"title": movie_title}},
                                       {"$project": {"frame": {"$arrayElemAt": ["$frames", frame_id]}}}])
    frame_info = list(frame_info)
    # TODO: it's assuming that the frame exists and it will be the first to be returned
    bounding_boxes = frame_info[0]["frame"]["Coordinates"]
    return bounding_boxes


def get_detection_shape(collection, movie_title):
    """
    Method to retrieve the size of the frames used when running the detection algorithm
    :param collection: MongoDB collection which stores a document for each movie with its own array of frames
    :param movie_title: title of the movie whose frame is to retrieve
    :return detection_shape: shape of the frames used for formerly running the detection algorithm
    """

    height_doc = collection.aggregate([{"$match": {"title": movie_title}},
                                       {"$project": {"height": {"$arrayElemAt": ["$detection_size", 0]}}}])
    width_doc = collection.aggregate([{"$match": {"title": movie_title}},
                                      {"$project": {"width": {"$arrayElemAt": ["$detection_size", 1]}}}])
    height_doc = height_doc.next()
    width_doc = width_doc.next()
    height = height_doc["height"]
    width = width_doc["width"]
    detection_shape = (height, width)
    print(detection_shape)
    return detection_shape
