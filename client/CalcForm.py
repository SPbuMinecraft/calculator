from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class CalcForm(FlaskForm):
    expression = StringField("Enter the expression to calculate", validators=[DataRequired()])
    submit = SubmitField("Calculate")
