from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class InputForm(FlaskForm):
  inputValue = StringField('Input')
  submit = SubmitField('Submit')
