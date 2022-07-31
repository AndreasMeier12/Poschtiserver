import wtforms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class AddListForm(FlaskForm):
    list_name = StringField('List name', validators=[DataRequired()])
    submit = SubmitField(label='Add!')


class TokenValidityForm(FlaskForm):
    token_validity_field = IntegerField('validityDuration',
                                        validators=[DataRequired()])
    token_validity_submit = SubmitField(label='Set!')


class DeleteListForm(FlaskForm):
    submit = SubmitField(label='Delete!')


class AddItemForm(FlaskForm):
    item = StringField('Name', validators=[DataRequired()])
    quantity = StringField('Quantity')
    shop = StringField('Shop')

    submit = SubmitField(label='Add!')


class DeleteAccountForm(FlaskForm):
    confirmation = StringField('Confirmation phrase',
                               validators=[DataRequired()])
    submit = SubmitField(label='☢')


class EditItemForm(FlaskForm):
    item_old = HiddenField()
    item = StringField('Name', validators=[DataRequired()])
    quantity_old = HiddenField()
    quantity = StringField('Quantity')
    shop_old = HiddenField()
    shop = StringField('Shop')

    submit = SubmitField(label='Add!')
