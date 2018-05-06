import json
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from datetime import datetime


class PrescriptionItem(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    drug = db.Column(db.String(60))
    duration = db.Column(db.Integer, index=True, unique=False)
    frequency = db.Column(db.Integer, index=True, unique=False)
    instruction = db.Column(db.String(60))
    prescription_id = db.Column(db.BigInteger, db.ForeignKey('prescription.id'))

    def __repr__(self):
        return '<PrescriptionItem: {} {} >'.format(self.duration, self.frequency, self.instruction)


class Prescription(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patient.id'))
    prescription_items = db.relationship('PrescriptionItem', backref='prescription', lazy='dynamic')
    doctor = db.Column(db.String(60))
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    @staticmethod
    def get_all():
        return Prescription.query.all()

    def __repr__(self):
        return "<Prescription: {}>".format(self.mobile_number)


class MedicalCondition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bp = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    special_conditions = db.Column(db.String(100))
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patient.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())


class Patient(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(60), index=True, unique=False)
    last_name = db.Column(db.String(60), index=True, unique=False)
    national_id = db.Column(db.String(60), index=True, unique=True)
    mobile_number = db.Column(db.String(10), index=True, unique=True)
    address = db.Column(db.String(150), index=True, unique=False)
    prescriptions = db.relationship('Prescription', backref='patient', lazy='dynamic')
    payments = db.relationship('Payment', backref='patient', lazy='dynamic')
    medical_conditions = db.relationship('MedicalCondition', backref='patient', lazy='dynamic')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def get(self, patient_id):
        return Patient.query.get(int(patient_id))

    @staticmethod
    def get_all():
        return Patient.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Patient: {}>".format(self.national_id)


class BillingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    payments = db.relationship('Payment', backref='billing_item', lazy='dynamic')

    def __repr__(self):
        return '<BillingItem: {}>'.format(self.name)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    billing_item_name = db.Column(db.String(60), db.ForeignKey('billing_item.name'))
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patient.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent password from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    # Set up user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


class Role(db.Model):
    """
    Create a Role table
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)
