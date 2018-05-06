from flask import abort, render_template
from flask_login import current_user, login_required, login_user, logout_user
from flask import flash, redirect, render_template, url_for, request
import json
from sqlalchemy.sql import text
from .. import db
from . import admin
from .forms import UserForm, RoleForm, UserAssignForm,  BillingItemForm
from ..models import User, Role, BillingItem


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# admin dashboard view
@admin.route('/dashboard')
@login_required
def dashboard():
    # prevent non-admins from accessing the page
    if not current_user.is_admin:
        abort(403)

    return render_template('admin/admin_dashboard.html', title="Dashboard")


@admin.route('/new_user', methods=['GET', 'POST'])
@login_required
def create_user():
    """
    Handle requests to the /new_user route
    Admin can add a new user to the database through the user form
    """

    form = UserForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        initial = "".join(item[0].lower() for item in first_name.split())
        password = initial + form.last_name.data.lower()

        user = User(email=form.email.data, username=form.username.data,
                    first_name=form.first_name.data, last_name=form.last_name.data,
                    password=password)

        # add user to the database
        db.session.add(user)
        db.session.commit()
        flash('User successfully created!')

        # redirect to the login page
        return redirect(url_for('admin.users'))

    # load registration template
    return render_template('admin/users/register.html', form=form, title='Create User')


@admin.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title="Users")


@admin.route('/users/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    """
    Delete a user from the database
    """
    check_admin()

    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('You have successfully deleted the user.')

    # redirect to the users page
    return redirect(url_for('admin.users'))


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a role to a user
    """
    check_admin()
    print("++++++++++++++++++++++++ Id", id)
    user = User.query.get_or_404(id)

    # prevent admin from being assigned a role
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a role.')

        # redirect to the users page
        return redirect(url_for('admin.users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')


# ----------------------------------- Role Views ---------------------------------------- #


@admin.route('/roles')
@login_required
def list_roles():
    check_admin()
    """
    List all roles
    """
    roles = Role.query.all()
    return render_template('admin/roles/roles.html',
                           roles=roles, title='Roles')


@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
    """
    Add a role to the database
    """
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,
                    description=form.description.data)

        try:
            # add role to the database
            db.session.add(role)
            db.session.commit()
            flash('You have successfully added a new role.')
        except:
            # in case role name already exists
            flash('Error: role name already exists.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    # load role template
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title='Add Role')


@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    """
    Edit a role
    """
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('You have successfully edited the role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_roles'))

    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/roles/role.html', add_role=add_role,
                           form=form, title="Edit Role")


@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    """
    Delete a role from the database
    """
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('You have successfully deleted the role.')

    # redirect to the roles page
    return redirect(url_for('admin.list_roles'))


@admin.route('/product/drug_search_list', methods=['GET', 'POST'])
def drug_search_list():
    search_term = request.args.get('search_term')
    print("+++++++++++ search term", search_term)
    search_term = ''.join((search_term, '%'))
    s = text("SELECT drug.name FROM drug WHERE drug.name LIKE :search_term")
    drugs = db.engine.execute(s, search_term=search_term).fetchall()
    print("+++++++++++++++++++++ DRUGS ", drugs)
    response = json.dumps(drugs)
    return response


@admin.route('/billing_items')
@login_required
def list_billing_items():
    check_admin()

    billing_items = BillingItem.query.all()
    return render_template('admin/billing/list.html',
                           billing_items=billing_items, title='Billing Items')


@admin.route('/billing_item/add', methods=['GET', 'POST'])
@login_required
def add_billing_item():
    check_admin()

    add_billing_item = True

    form = BillingItemForm()
    if form.validate_on_submit():
        billing_item = BillingItem(name=form.name.data, description=form.description.data)

        try:
            db.session.add(billing_item)
            db.session.commit()
            flash('You have successfully added a new billing item.')
        except:
            # in case role name already exists
            flash('Error: billing item  already exists.')

        return redirect(url_for('admin.list_billing_items'))

    # load role template
    return render_template('admin/billing/add.html', add_billing_item=add_billing_item,
                           form=form, title='Add Billing Item')


@admin.route('/billing_item/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_billing_item(id):

    check_admin()

    add_billing_item = False

    billing_item = BillingItem.query.get_or_404(id)
    form = BillingItemForm(obj=billing_item)
    if form.validate_on_submit():
        billing_item.name = form.name.data
        billing_item.description = form.description.data

        db.session.add(billing_item)
        db.session.commit()
        flash('You have successfully edited the billing item.')

        return redirect(url_for('admin.list_billing_items'))

    form.description.data = billing_item.description
    form.name.data = billing_item.name

    return render_template('admin/billing/add.html', add_billing_item=add_billing_item,
                           form=form, title="Edit Billing Item")


@admin.route('/billing_item/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_billing_item(id):

    check_admin()

    billing_item = BillingItem.query.get_or_404(id)
    db.session.delete(billing_item)
    db.session.commit()
    flash('You have successfully deleted the billing item.')

    return redirect(url_for('admin.list_billing_items'))
