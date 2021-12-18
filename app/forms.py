from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class AddListForm(FlaskForm):
    list_name = StringField('List name', validators=[DataRequired()])
    submit = SubmitField(label='Add!')


class DeleteListForm(FlaskForm):
    submit = SubmitField(label='Delete!')

class AddItemForm(FlaskForm):
    item = StringField('Name', validators=[DataRequired()])
    quantity = StringField('Quantity')
    shop = StringField('Shop')

    submit = SubmitField(label='Add!')
