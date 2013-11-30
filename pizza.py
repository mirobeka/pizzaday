from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
import chommi

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
  return redirect(url_for("welcome"))

@app.route("/welcome/")
def welcome():
  return render_template("welcome.jinja")

@app.route("/pizzaorder/")
def pizzaorder():
  pizzas = chommi.gimme_dat_pizzas()
  return render_template("select_pizza.jinja", pizzas=pizzas)

if __name__ == "__main__":
  app.run(host="0.0.0.0")
