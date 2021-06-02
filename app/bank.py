"""
Demonstrative online banking application for Flask-HoneyAuth

"""
import config

import flask
from flask import request, g

import logging

from werkzeug.security import generate_password_hash, check_password_hash

from flask_honeyauth import HTTPBasicAuth
import honeyroutes

app = flask.Flask(__name__)
CONFIG = config.configuration()

app.secret_key = b'super secret key'

auth = HTTPBasicAuth()

users = {
        "john": generate_password_hash("hello"),
        "susan": generate_password_hash("bye"),
        "dave": generate_password_hash("realdave")
}

honey_users = {
        "dave": generate_password_hash("imnotdave"),
        "alice": generate_password_hash("asdfghj"),
        "winston": generate_password_hash("honeybear")
}

# Authentication handlers
# this is where we define the logic to authenticate users and verify honeytokens

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        user = {"username": username, "payload": "x"}
        return user

@auth.check_honeytoken
def check_honeytoken(auth):
    if not auth or not auth.username:
        return False

    elif auth.username in honey_users and check_password_hash(honey_users.get(auth.username), auth.password):
        username = auth.username
        user = {"username": username, "payload": "x"}
        return user

    else:
        return False

# Main page entry
@app.route("/")
@app.route("/index")
@auth.login_required(honey=honeyroutes.honey_index)
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('index.html')

# error handler for 404s
@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
