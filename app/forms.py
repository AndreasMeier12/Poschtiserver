from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length

class AddListForm(FlaskForm):
    list_name = StringField('List name', validators=[DataRequired()])
    submit = SubmitField(label='Add!')

class TokenValidityForm(FlaskForm):
    token_validity_field = IntegerField('validityDuration', validators=[DataRequired()])
    token_validity_submit = SubmitField(label='Set!')




class DeleteListForm(FlaskForm):
    submit = SubmitField(label='Delete!')

class AddItemForm(FlaskForm):
    item = StringField('Name', validators=[DataRequired()])
    quantity = StringField('Quantity')
    shop = StringField('Shop')

    submit = SubmitField(label='Add!')
