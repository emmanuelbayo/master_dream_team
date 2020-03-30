from flask import abort, render_template, url_for, redirect
from flask_login import current_user,login_required

from . import home

@home.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    return render_template('home/admin_dashboard.html', title = "Tableau de bord admin")

@home.route('/')
def homepage():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('home.admin_dashboard'))
        else:
            return redirect(url_for('home.dashboard'))
    return render_template('home/index.html',title="Bienvenue")

@home.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        abort(403)
    return render_template('home/dashboard.html',title="Tableau de bord")

