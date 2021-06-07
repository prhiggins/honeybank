import flask
from flask import request, g
from database_manager import HoneyDBManager

app = flask.Flask(__name__)

db = HoneyDBManager()

def honey_index():
    app.logger.debug("Honey -- Main page entry, user {}".format(g.flask_httpauth_user["username"]))

    username = g.flask_httpauth_user["username"]
    balance = db.get_balance_for_user(username)

    transactions = db.get_transactions_for_user(username)

    return flask.render_template('index.html', balance=balance, tx_history=transactions)

def honey_transfer():
    app.logger.debug("Honey -- transfer")
    username = g.flask_httpauth_user["username"]
    balance = db.get_balance_for_user(username)

    recipient = request.form['recipient']
    amount = float(request.form['amount'])

    if db.transfer(amount, recipient, username) is not None:
        return flask.render_template('success.html')

    return flask.render_template('failure.html')

def honey_transfer_form():
    app.logger.debug("Honey -- transfer form")
    username = g.flask_httpauth_user["username"]
    balance = db.get_balance_for_user(username)

    return flask.render_template('transfer.html', balance=balance)
