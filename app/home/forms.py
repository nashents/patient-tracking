from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, FloatField, IntegerField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Patient, BillingItem


class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    national_id = StringField('National ID', validators=[DataRequired()])
    mobile_number = StringField('Mobile Number', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])

    submit = SubmitField('Register', id='submit_button')

    @staticmethod
    def validate_national_id(self, field):
        if Patient.query.filter_by(national_id=field.data).first():
            raise ValidationError('Customer is already registered')


class CustomerAccountForm(FlaskForm):
    mobile_number = StringField('Number')
    max_value_for_transaction = StringField('Threshold', validators=[DataRequired()])
    submit = SubmitField('Update')


class PrescriptionItemForm(FlaskForm):
    drug = StringField('Drug', validators=[DataRequired()])
    instructions = StringField('Instructions', validators=[DataRequired()])
    frequency = StringField('Frequency', validators=[DataRequired()])
    duration = IntegerField('Duration', validators=[DataRequired()])
    submit = SubmitField('Save')


class PaymentForm(FlaskForm):
    billing_item = QuerySelectField(query_factory=lambda: BillingItem.query.all(),
                                    get_label="name")
    amount = FloatField('Amount', validators=[DataRequired()])
    submit = SubmitField('Save')


class MedicalConditionForm(FlaskForm):
    bp = FloatField('Blood Pressure(BP)', validators=[DataRequired()])
    temperature = FloatField('Temperature', validators=[DataRequired()])
    special_conditions = StringField('Special Conditions', validators=[DataRequired()])
    submit = SubmitField('Save')