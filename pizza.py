from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import g
from flask import session as flask_session
import sessions
import sqlite3
import os
import logging

logger = logging.getLogger("CONTROLLER")

DATABASE = 'das_pizzas.db'
app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    return redirect(url_for("welcome"))

@app.route("/welcome/")
def welcome():
    return render_template("welcome.jinja")

@app.route("/orderpizza/", methods=["GET"])
def get_pizzaorder():
    # run before request
    if "active_session" not in flask_session:
        return redirect(url_for("get_active_sessions"))

    session_id = flask_session["active_session"]
    pizzas = get_pizza_options(session_id)
    return render_template("select_pizza.jinja", pizzas=pizzas)

@app.route("/orderpizza/", methods=["POST"])
def create_pizzaorder():
    # run before request
    if "active_session" not in flask_session:
        return url_for("get_active_sessions")

    session_id = flask_session["active_session"]
    sessions.add_order(session_id, request.form)
    return url_for("thank_you")

@app.route("/thank_you/")
def thank_you(session_name, size, pizza):
    flask_session.pop("active_session")
    return render_template("thank_you.jinja")

@app.route("/startsession/", methods=["GET"])
def get_startsession():
    pizza_places = sessions.pizza_places()
    return render_template("start_session.jinja", pizza_places=pizza_places)

@app.route("/startsession/", methods=["POST"])
def create_session():
    session_id= sessions.create_session(request.form)
    flask_session["active_session"] = session_id
    return url_for("get_pizzaorder")

@app.route("/activesessions/", methods=["GET"])
def get_active_sessions():
  session_list = sessions.get_session_list()
  return render_template("active_sessions.jinja", sessions=session_list)

@app.route("/activesessions/", methods=["POST"])
def join_session():
    flask_session["active_session"] = request.form["session"]
    return url_for("get_pizzaorder")

# Database helpers
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    db.row_factory = sqlite3.Row
    return db

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def check_database():
    if not os.path.exists(DATABASE):
        with open(DATABASE, "w"):
            logger.info("Creating empty database file: {}".format(DATABASE))
            init_db()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def connect_to_database():
    try:
        connection = sqlite3.connect(DATABASE)
    except sqlite3.Error as e:
        logger.exception("Exception while connecting to database: {}".format(DATABASE))
        logger.exception(e)
        raise e
    return connection

if __name__ == "__main__":
    check_database()
    #app.run() # listen on localhost / more secure
    app.run(host="127.0.0.1") # listen on all public IPs
