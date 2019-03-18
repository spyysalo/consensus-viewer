import os

from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py', silent=True)

    from . import db
    db.init(app)

    from . import view
    app.register_blueprint(view.bp)
    
    return app
