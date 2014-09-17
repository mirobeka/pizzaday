from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import session as flask_session
import sessions
import pkgutil

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

if __name__ == "__main__":
  #app.run() # listen on localhost / more secure
  app.run(host="127.0.0.1") # listen on all public IPs
