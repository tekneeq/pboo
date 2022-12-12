import os

from . import db
from . import bp_auth
from flask import Flask

def create_app(test_config=None):
    # create and configure the pboo
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')

    # instance_path
    # https://flask.palletsprojects.com/en/2.1.x/config/#instance-folders
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'pboo.sqlite'),
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

    @app.route("/")
    def hello():
        return "Hello, World!"

    @app.route('/user/<name>')
    def user(name):
        return '<h1>Hellooo, {}!</h1>'.format(name)

    db.init_app(app)

    app.register_blueprint(bp_auth.bp)

    return app