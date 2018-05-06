from flask import render_template, redirect, flash, url_for
from flask_login import login_required, current_user

from . import home
from .forms import RegistrationForm, PaymentForm, MedicalConditionForm, PrescriptionItemForm
from ..models import Patient, Payment, MedicalCondition, Prescription, PrescriptionItem
from app import db


@home.route('/')
def index():
    return redirect('/login')


@home.route('/patient', methods=['GET', 'POST'])
@login_required
def add_patient():
    form = RegistrationForm()
    if form.validate_on_submit():

        patient = Patient(first_name=form.first_name.data, last_name=form.last_name.data,
                          national_id=form.national_id.data, mobile_number=form.mobile_number.data,
                          address=form.address.data)
        patient.save()
        return redirect('/patients')

    else:
        return render_template('home/patient/patient.html', form=form, title='Add Customer')


@home.route('/patients', methods=['GET', 'POST'])
@login_required
def list_patients():
    patients = Patient.get_all()
    return render_template('home/patient/patients.html', patients=patients, title='Patients')


@home.route('/patient/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    """
    Edit a patient
    """

    add_patient = False

    patient = Patient.query.get_or_404(id)
    form = RegistrationForm(obj=patient)
    if form.validate_on_submit():
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.national_id = form.national_id.data
        db.session.commit()
        flash('You have successfully edited the patient.')

        # redirect to the customers page
        return redirect(url_for('home.list_patients'))

    form.first_name.data = patient.first_name
    form.last_name.data = patient.last_name
    form.national_id.data = patient.national_id
    return render_template('home/patient/patient.html', action="Edit",
                           add_patient=add_patient, form=form,
                           patient=patient, title="Edit Patient")


@home.route('/customers/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_patient(id):
    """
    Delete a patient from the database
    """

    patient = Patient.query.get_or_404(id)
    patient.delete()
    flash('You have successfully deleted the patient.')

    # redirect to the patient page
    return redirect(url_for('home.list_patients'))


@home.route('/patient/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view_patient(id):
    """
    View a patient profile
    """
    patient = Patient.query.get(int(id))
    payments = Payment.query.filter_by(patient_id=id).all()
    medical_conditions = MedicalCondition.query.filter_by(patient_id=id).all()
    prescriptions = Prescription.query.filter_by(patient_id=id).all()
    return render_template('home/patient/patient_profile.html', patient=patient,
                           payments=payments, medical_conditions=medical_conditions,
                           prescriptions=prescriptions, title='Patient Profile')


@home.route('/patient/new_prescription/<int:id>', methods=['GET', 'POST'])
@login_required
def new_prescription(id):

        prescription = Prescription(doctor=current_user.first_name + " " + current_user.last_name,
                                    patient_id=id)
        db.session.add(prescription)
        db.session.commit()
        flash("Empty Prescription successfully created!")
        return redirect(url_for('home.view_patient', id=id))


@home.route('/patient/new_payment/<int:id>', methods=['GET', 'POST'])
@login_required
def new_payment(id):
    patient = Patient.query.get(int(id))

    form = PaymentForm()
    if form.validate_on_submit():

        payment = Payment(amount=form.amount.data, billing_item=form.billing_item.data)
        patient.payments.append(payment)
        patient.save()
        return redirect(url_for('home.view_patient', id=id))

    else:
        return render_template('home/patient/payment/add.html', form=form, title='Add Medical Condition')


@home.route('/patient/new_medical_condition/<int:id>', methods=['GET', 'POST'])
@login_required
def new_medical_condition(id):
    patient = Patient.query.get(int(id))

    form = MedicalConditionForm()
    if form.validate_on_submit():

        medical_condition = MedicalCondition(bp=form.bp.data, temperature=form.temperature.data,
                                             special_conditions=form.special_conditions.data)
        patient.medical_conditions.append(medical_condition)
        patient.save()
        return redirect(url_for('home.view_patient', id=id))

    else:
        return render_template('home/patient/medical_condition/add.html', form=form, title='Add Medical Condition')


@home.route('/patient/medical_condition/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_medical_condition(id):

    new_medical_condition = False

    medical_condition = MedicalCondition.query.filter_by(patient_id=id).first()

    print("+++++++++++++++++++++++++", medical_condition)
    form = MedicalConditionForm(obj=medical_condition)
    if form.validate_on_submit():
        medical_condition.bp = form.bp.data
        medical_condition.temperature = form.temperature.data
        medical_condition.special_conditions = form.special_conditions.data
        db.session.commit()
        flash('You have successfully edited the medical conditions.')

        return redirect(url_for('home.view_patient', id=id))

    form.bp.data = medical_condition.bp
    form.temperature.data = medical_condition.temperature
    form.special_conditions.data = medical_condition.special_conditions
    return render_template('home/patient/medical_condition/add.html', action="Edit",
                           new_medical_condition=new_medical_condition, form=form,
                           medical_condition=medical_condition, title="Edit Medical Conditions")


@home.route('/patient/prescription/prescription_items/<int:id>', methods=['GET', 'POST'])
def list_prescription_items(id):

    prescription = Prescription.query.get(int(id))
    patient = Patient.query.get(int(prescription.patient_id))
    prescription_items = PrescriptionItem.query.filter_by(prescription_id=id).all()

    return render_template('home/patient/prescription/items/list.html', prescription=prescription,
                           prescription_items=prescription_items, patient=patient,
                           title='Prescription Items')


@home.route('/patient/prescription/prescription_item/<int:id>', methods=['GET', 'POST'])
def add_prescription_item(id):

    prescription = Prescription.query.get(int(id))
    patient = Patient.query.get(int(prescription.patient_id))

    form = PrescriptionItemForm()
    if form.validate_on_submit():
        prescription_item = PrescriptionItem(drug=form.drug.data, duration=form.duration.data,
                                             frequency=form.frequency.data, instruction=form.instructions.data)
        prescription.prescription_items.append(prescription_item)
        db.session.commit()
        flash('Successfully added the prescription item to the prescription!.')

        return redirect(url_for('home.list_prescription_items', id=id))

    else:
        return render_template('home/patient/prescription/items/add.html', form=form,
                               title='Add Prescription Item')
