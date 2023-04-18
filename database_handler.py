import pymongo
from urllib.parse import quote_plus


def db_connection(username, password):
    """
    Method to instantiate a connection to a MongoDB Atlas instance
    :param username: username to access the database
    :param password: password to access the database
    :return client: a client connected to the database instance
    """
    username = quote_plus(username)
    password = quote_plus(password)
    cluster = 'cluster0.hns6k.mongodb.net'
    options = '/authSource=admin?ssl=true&tlsAllowInvalidCertificates=true'
    uri = 'mongodb+srv://' + username + ':' + password + '@' + cluster + options
    client = pymongo.MongoClient(uri)
    return client


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
