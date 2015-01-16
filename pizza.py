from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import g
from flask import session as flask_session
from contextlib import closing
from functools import wraps
from datetime import datetime
import sessions
import sqlite3
import os
import logging
from forms import EnterEmailForm, StartSessionForm

def email_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_email" not in flask_session:
            return redirect(url_for("enter_email_get"))
        return f(*args, **kwargs)
    return decorated_function

def session_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "active_session" not in flask_session:
            return redirect(url_for("startsession"))
        return f(*args, **kwargs)
    return decorated_function

logger = logging.getLogger("CONTROLLER")

app = Flask(__name__)
app.config.from_envvar("PIZZA_CONFIG")

@app.route("/", methods=["POST"])
def enter_email_post():
    emailform = EnterEmailForm()
    if emailform.validate_on_submit():
        flask_session["user_email"] = emailform.data["email"]
        return redirect(url_for("select_action"))
    return render_template("enter_email.jinja", emailform=emailform)

@app.route("/", methods=["GET"])
def enter_email_get():
    emailform = EnterEmailForm()
    return render_template("enter_email.jinja", emailform=emailform)

@app.route("/select/")
@email_required
def select_action():
    return render_template("select_action.jinja")

@app.route("/orderpizza/", methods=["GET"])
@email_required
@session_required
def get_pizzaorder():
    # run before request
    session_id = flask_session["active_session"]
    pizzas = sessions.pizzas(session_id)
    print(pizzas)
    return render_template("select_pizza.jinja", pizzas=pizzas)

@app.route("/orderpizza/", methods=["POST"])
@email_required
@session_required
def create_pizzaorder():
    if "pizza_id" in request.form:
        pizza_id = int(request.form["pizza_id"])
        pizza_extra = request.form["extra"]
        session_id = flask_session["active_session"]
        user_email = flask_session["user_email"]
        sessions.add_order(session_id, user_email, pizza_id, pizza_extra)
        return redirect(url_for("thank_you"))

    return url_for("thank_you")

@app.route("/thank_you/")
@email_required
@session_required
def thank_you():
    session_id = flask_session.pop("active_session")
    user_email = flask_session.pop("user_email")

    order = sessions.get_order(session_id, user_email)

    return render_template("thank_you.jinja", order=order)

@app.route("/startsession/", methods=["GET"])
@email_required
def get_startsession():
    form = StartSessionForm()
    return render_template("start_session.jinja", form=form)

@app.route("/startsession/", methods=["POST"])
def create_session():
    form = StartSessionForm()
    if form.validate_on_submit():
        session_id = sessions.create_session(flask_session["user_email"], form.data)
        flask_session["active_session"] = session_id
        return redirect(url_for("get_active_sessions"))
    return render_template("start_session.jinja", form=form)

@app.route("/dashboard/", methods=["GET"])
@email_required
@session_required
def session_dashboard():
    session_id = flask_session["active_session"]
    session_data = sessions.get_session(session_id)
    return render_template("session_dashboard.jinja", orders=session_data["orders"])

@app.route("/dashboard/deleteorder", methods=["POST"])
@email_required
@session_required
def session_dashboard_action():
    order_id = int(request.form["order_id"])
    sessions.delete_order(order_id)
    return redirect(url_for("session_dashboard"))

@app.route("/activesessions/", methods=["GET"])
@email_required
def get_active_sessions():
  session_list = sessions.get_session_list()
  return render_template("active_sessions.jinja", sessions=session_list)

@app.route("/activesessions/", methods=["POST"])
def join_session():
    flask_session["active_session"] = request.form["session_id"]
    return redirect(url_for("get_pizzaorder"))

# Database helpers
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with closing(connect_to_database()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def check_database():
    DATABASE = app.config["DATABASE"]
    if not os.path.exists(DATABASE):
        with open(DATABASE, "w"):
            print("Creating empty database file: {}".format(DATABASE))
            init_db()

def sql_query(query):
    db = get_db()
    db.execute(query)
    db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def connect_to_database():
    DATABASE = app.config["DATABASE"]
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
