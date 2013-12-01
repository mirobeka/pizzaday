from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
import sessions

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
  return redirect(url_for("welcome"))

@app.route("/welcome/")
def welcome():
  return render_template("welcome.jinja")

@app.route("/<session_name>/orderpizza/")
def pizzaorder(session_name):
  session = sessions.get_session(session_name)
  restaurant_name = session.get("info", "restaurant")
  restaurant = __import__("pizza_places."+restaurant_name, fromlist=[restaurant_name])
  pizzas = restaurant.gimme_dat_pizzas()
  return render_template("select_pizza.jinja", pizzas=pizzas)

@app.route("/startsession/", methods=["GET", "POST"])
def start_session():
  if request.method == "POST":
    return start_new_session(request)
  else:
    return render_template("start_session.jinja")

@app.route("/activesessions/")
def active_sessions():
  session_list = sessions.get_session_list()
  if len(session_list) <= 0:
    return render_template("no_active_sessions.jinja")
  return render_template("active_sessions.jinja", sessions=session_list)


##
# Functions

def start_new_session(request):
  sessions.create_session(request.form["session_name"], request.form)
  return redirect_to(url_for("active_sessions"))

if __name__ == "__main__":
  app.run()
