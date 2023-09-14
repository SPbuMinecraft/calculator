from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class CalcForm(FlaskForm):
    expression = StringField("Enter the expression to calculate")
    submit = SubmitField("Calculate")