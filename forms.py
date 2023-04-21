from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields import DateField
from wtforms.validators import DataRequired

class StockForm(FlaskForm):
    symbol = StringField('Stock Symbol', validators=[DataRequired()])
    start_date = DateField('Start Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('End Date (YYYY-MM-DD)', format='%Y-%m-%d', validators=[DataRequired()])
