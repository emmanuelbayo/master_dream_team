from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user,current_user

from . import auth
from .forms import LoginForm, RegistrationForm
from .. import db
from ..models import Employee


@auth.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('home.admin_dashboard'))
        return redirect(url_for('home.dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        employee = Employee(email=form.email.data,
                            username=form.username.data,
                            first_name=form.first_name.data,
                            last_name=form.last_name.data,
                            password=form.password.data)

        
        db.session.add(employee)
        db.session.commit()
        flash('Vous vous êtes inscrits avec succès ! Vous pouvez vous connecter maintenant.')

        
        return redirect(url_for('auth.login'))

   
    return render_template('auth/register.html', form=form, title='Inscription')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('home.admin_dashboard'))
        return redirect(url_for('home.dashboard'))
    form = LoginForm()
    
    if form.validate_on_submit():
        employee = Employee.query.filter_by(email=form.email.data).first()
        if employee is not None and employee.verify_password(form.password.data):
            login_user(employee)
            if employee.is_admin:
                return redirect(url_for('home.admin_dashboard'))
            else:
                return redirect(url_for('home.dashboard'))
        else:
            flash('Mot de passe or email invalide')

    return render_template('auth/login.html', form=form, title='Connexion')


@auth.route('/logout')
@login_required
def logout():
    """
    Handle requests to the /logout route
    Log an employee out through the logout link
    """
    logout_user()
    flash("Vous êtes bien déconnectés")

    return redirect(url_for('auth.login'))