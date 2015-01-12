from flask.ext.wtf import Form
from wtforms import StringField, DateTimeField, SelectField
from wtforms.validators import Length
from datetime import datetime

class EnterEmailForm(Form):
    email = StringField('Email Address', validators=[Length(min=6, max=35)])

class StartSessionForm(Form):
    date_format = "%Y-%m-%d %H:%M"
    deadline = DateTimeField("deadline", format=date_format)
    recipients = StringField("recipients")
    pizza_place = SelectField("pizza_place", choices=[("carla","Carla"),("chommi","Chommi"), ("erik","Erik")], default="carla")
