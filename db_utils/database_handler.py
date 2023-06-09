import time
import pymongo
from urllib.parse import quote_plus
import json
from bson.objectid import ObjectId
import pprint
import numpy as np
import base64
import pandas as pd
from tqdm import tqdm


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


def create_movie_document(movie_json_file):
    """
    Method to create a document to be inserted in the MongoDB collection
    :param movie_json_file: json file containing the information about the movie
    :return document: document to be inserted in the MongoDB collection
    """
    frame_ids = []
    document = {}
    for key in movie_json_file.keys():
        try:
            frame_ids.append(int(key))
        except ValueError:
            document[key] = movie_json_file[key]
    #TODO tune the item description when uploading the movie document
    item_description = "grey t-shirt"
    document['frames'] = [
        {"_id": ObjectId(frame_id.to_bytes(12, 'big')),
         "Coordinates": [(np.array(movie_json_file[str(frame_id)][box_id]['Coordinates'])*document['detection_size'][0]).tolist()
                         for box_id in movie_json_file[str(frame_id)].keys()],
         "Items": [item_description for _ in movie_json_file[str(frame_id)].keys()]}
                         for frame_id in frame_ids]
    return document


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


def get_frame_bounding_boxes(collection, movie_title, frame_id):
    """
    Method to retrieve the bounding boxes associated to a frame in a movie
    :param collection: MongoDB collection which stores a document for each movie with its own array of frames
    :param movie_title: title of the movie whose frame is to retrieve
    :param frame_id: id of the frame to retrieve
    :return bounding_boxes: bounding boxes associated to the requested frame_id
    """
    movie_title = movie_title.replace("_", " ").lower()
    frame_info = collection.aggregate([{"$match": {"title": movie_title}},
                                       {"$project": {"frame": {"$arrayElemAt": ["$frames", frame_id]}}}])
    frame_info = list(frame_info)
    # TODO: it's assuming that the frame exists and it will be the first to be returned
    bounding_boxes = frame_info[0]["frame"]["Coordinates"]
    return bounding_boxes


def get_detection_fps(collection, movie_title):
    """
    Method used to retrieve the fps used when running the detection algorithm
    :param collection: MongoDB collection which stores a document for each movie with its own array of frames
    :return detection_fps: fps used by the detection algorithm
    """
    documents = list(collection.find({"title": movie_title}, {"detection_fps": 1, "fps": 1, "_id": 0}))
    assert len(documents) == 1
    return documents[0]["detection_fps"], documents[0]["fps"]


def get_movie_product(collection, movie_title):
    """
    Method used to retrieve the products associated to a movie
    :param collection: MongoDB collection which stores a document for each movie with its details
    :param movie_title: title of the movie whose products are to retrieve
    :return: the list of subdocuments containing the products associated to the movie with their link and name
    """
    documents = list(collection.find({"title": movie_title}, {"products": 1, "_id": 0}))
    assert len(documents) == 1

    product_link = []
    for product in documents[0]["products"]:
        subdocument = list(collection.find({str(product)+".name": str(product)}, {str(product)+".name": 1,
                                                                             str(product)+".link": 1,
                                                                             "_id": 0}))
        product_link.append({subdocument[0][str(product)]["name"]: subdocument[0][str(product)]["link"]})

    return product_link


if __name__ == '__main__':
    db_client = db_connection('Piero_Rendina', 'R3nd1n@2021')
    movies_collection = db_client.movies.movies_info
    doc = create_movie_document(json.load(open("../json_files/bruce_banner_tony_stark.json")))
    movies_collection.insert_one(doc)
