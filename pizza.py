from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
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

@app.route("/<session_name>/orderpizza/", methods=["GET", "POST"])
def pizzaorder(session_name):
  if request.method == "POST":
    sessions.add_order_to_session(session_name, request.form)
    return url_for("review_order", session_name=session_name, pizza=request.form["pizza"])
  else:
    return show_pizza_options(session_name)

@app.route("/<session_name>/review/<size>/<pizza>/")
def review_order(session_name, pizza):
  return render_tempalte("review_order.jinja", pizza=pizza)

@app.route("/startsession/", methods=["GET", "POST"])
def start_session():
  if request.method == "POST":
    return start_new_session(request)
  else:
    pizza_places = get_list_of_pizza_places()
    return render_template("start_session.jinja", pizza_places=pizza_places)

@app.route("/activesessions/")
def active_sessions():
  session_list = sessions.get_session_list()
  if len(session_list) <= 0:
    return render_template("no_active_sessions.jinja")
  return render_template("active_sessions.jinja", sessions=session_list)


##
# Functions

def show_pizza_options(session_name):
    session = sessions.get_session(session_name)
    restaurant_name = session.get("info", "restaurant")
    restaurant = __import__("pizza_places."+restaurant_name, fromlist=[restaurant_name])
    pizzas = restaurant.gimme_dat_pizzas()
    return render_template("select_pizza.jinja", pizzas=pizzas)


def start_new_session(request):
  sessions.create_session(request.form["email"], request.form)
  return url_for("active_sessions")

def get_list_of_pizza_places():
  return [name for _, name, _ in pkgutil.iter_modules(["pizza_places"])]

if __name__ == "__main__":
  app.run()
