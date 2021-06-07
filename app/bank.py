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
from database_manager import DBManager

import time

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

# set up the mock database
db = DBManager()
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
    username = g.flask_httpauth_user["username"]
    balance = db.get_balance_for_user(username)

    transactions = db.get_transactions_for_user(username)

    return flask.render_template('index.html', balance=balance, tx_history=transactions)

# for making transfers
@app.route("/transfer", methods=['POST'])
@auth.login_required(honey=honeyroutes.honey_transfer)
def transfer():
    app.logger.debug("transfer submitted")
    username = g.flask_httpauth_user["username"]
    balance = db.get_balance_for_user(username)

    recipient = request.form['recipient']
    amount = float(request.form['amount'])

    try:
        result = db.transfer(amount, recipient, username)
    except KeyError as e:
        return flask.render_template('failure.html')
        
    if result is not None:
        return flask.render_template('success.html')

    return flask.render_template('failure.html')

# for making transfers
@app.route("/transfer_form")
@auth.login_required(honey=honeyroutes.honey_transfer_form)
def transfer_form():
    app.logger.debug("transfer page reached")
    username = g.flask_httpauth_user["username"]
    balance = db.get_balance_for_user(username)

    return flask.render_template('transfer.html', balance=balance)

# error handler for 404s
@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] = flask.url_for("index")
    return flask.render_template('404.html'), 404

@app.context_processor
def datetime_processor():
    def format_date(utc_seconds):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(utc_seconds))

    return dict(format_date=format_date)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
