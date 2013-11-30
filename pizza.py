from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
import chommi
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
  restaurant = __import__(session.get("info", "restaurant"))
  pizzas = restaurant.gimme_dat_pizzas()
  return render_template("select_pizza.jinja", pizzas=pizzas)

@app.route("/startsession/")
def start_session():
  return render_template("start_session.jinja")

@app.route("/activesessions/")
def start_pizza_session():
  session_list = sessions.get_session_list()
  if len(session_list) <= 0:
    return render_template("no_active_sessions.jinja")
  return render_template("active_sessions.jinja", sessions=session_list)

if __name__ == "__main__":
  app.run()
