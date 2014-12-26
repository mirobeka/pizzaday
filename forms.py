from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import Length

class EnterEmailForm(Form):
    email  = StringField('Email Address', validators=[Length(min=6, max=35)])
