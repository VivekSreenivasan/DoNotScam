from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField

class InputForm(FlaskForm):
  inputValue = TextAreaField('Input')
  submit = SubmitField('Submit')
