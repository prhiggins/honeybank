import flask
from flask import request, g

app = flask.Flask(__name__)

def honey_index():
    app.logger.debug("Honey -- Main page entry, user {}".format(g.flask_httpauth_user["username"]))
    return flask.render_template('index.html')
