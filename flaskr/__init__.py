import os
from flask import Flask
from db_utils.database_handler import get_db_uri


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # set up the credentials for the MongoDB database instance
    mongo_uri = get_db_uri('Piero_Rendina', 'R3nd1n@2021')
    app.config.from_mapping(
        SECRET_KEY='dev', threaded=True,
        MONGO_URI=mongo_uri,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth
    app.register_blueprint(auth.bp)

    from . import movies
    app.register_blueprint(movies.bp)
    app.add_url_rule('/', endpoint='index')
    return app
