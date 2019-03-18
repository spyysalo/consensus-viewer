import os

from flask import Flask
from flask import Response, url_for


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_pyfile('config.py', silent=True)

    from . import db
    db.init(app)

    from . import view
    app.register_blueprint(view.bp)

    # From https://stackoverflow.com/a/13318415, TODO move
    @app.route("/routes")
    def routes():
        import urllib.parse
        output = []
        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)
            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.parse.unquote("{:50s} {:20s} {}".format(
                rule.endpoint, methods, url))
            output.append(line)
        return Response('\n'.join(sorted(output)), mimetype='text/plain')
    
    return app
