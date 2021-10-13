from flask_wtf import FlaskForm
from wtforms.fields.core import StringField, FloatField
from wtforms.validators import DataRequired, NumberRange

class Movimiento(FlaskForm):
    From = StringField( "From", validators=[DataRequired(message="")])



    To =
    Amount = FloatField( "Amount", validators=[DataRequired(message=""), NumberRange(message="Debe introducir un numero positivo", min = 0.01)])