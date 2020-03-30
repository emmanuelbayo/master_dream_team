from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import DepartementForm, RoleForm, EmployeeAssignForm
from .. import db
from .. models import Department, Role, Employee

def check_admin():
    if not current_user.is_admin:
        abort(403)

@admin.route('/departments', methods=['GET','POST'])
@login_required
def list_departments():
    """
    Liste des departements
    """
    check_admin()

    departments = Department.query.all()

    return render_template('admin/departement/departements.html', title="Departements", departments=departments)

@admin.route('/departments/add', methods=['GET','POST'])
@login_required
def add_department():

    check_admin()
    
    add_department = True

    form = DepartementForm()

    if form.validate_on_submit():
        department = Department(name=form.name.data,description=form.description.data)
        try:
            db.session.add(department)
            db.session.commit()
            flash('Le nouveau département a été ajouté avec succès !')
        except:
            flash('Erreur : Ce département existe déjà')
        
        return redirect(url_for('admin.list_departments'))
    
    return render_template('admin/departement/departement.html',action="Add",
                            add_department = add_department, form=form, title="Ajouter Departement")

@admin.route('/departments/edit/<int:id>',methods=['GET', 'POST'])
@login_required
def edit_department(id):

    check_admin()

    add_department = False

    department = Department.query.get_or_404(id)
    form = DepartementForm(obj=department)

    if form.validate_on_submit():
        department.name = form.name.data
        department.description = form.description.data
        db.session.commit()
        flash('La modification du département a été effectué avec succès')

        return redirect(url_for('admin.list_departments'))
    
    form.name.data=department.name
    form.description.data = department.description

    return render_template('admin/departement/departement.html',action="Edit",
                            add_department=add_department,form=form, title='Modifier Departement')

@admin.route('/departments/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_department(id):

    check_admin()

    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()

    flash('La suppression du departement a été effectuée avec succès !')

    return redirect(url_for('admin.list_departments'))

@admin.route('/roles')
@login_required
def list_roles():
    check_admin() 

    roles = Role.query.all()
    return render_template('admin/role/roles.html', roles=roles, title="Roles")

@admin.route("/roles/add",methods=['GET','POST']) 
@login_required
def add_role():
    check_admin()

    add_role = True

    form = RoleForm()
    if form.validate_on_submit():
        role = Role(name=form.name.data,description=form.description.data)

        try:
            db.session.add(role)
            db.session.commit()
            flash("Le nouveau poste a été créé avec succès")
        except:
            flash("Erreur: Ce poste existe déjà dans l'équipe")

        return redirect(url_for('admin.list_roles'))
    
    return render_template('admin/role/role.html',add_role = add_role,
                            form=form,title="Créer un poste")
@admin.route('/roles/edit/<int:id>', methods=['GET','POST'])
@login_required
def edit_role(id):
    check_admin()

    add_role = False

    role = Role.query.get_or_404(id)
    form = RoleForm(obj=role)
    if form.validate_on_submit():
        role.name = form.name.data
        role.description = form.description.data
        db.session.add(role)
        db.session.commit()
        flash('Vos modifications ont été effectué !')

        return redirect(url_for('admin.list_roles'))
    
    form.description.data = role.description
    form.name.data = role.name
    return render_template('admin/role/role.html', add_role=add_role,
                            form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
    check_admin()

    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    flash('La suppression a été effectué avec succès!')

    return redirect(url_for('admin.list_roles'))

@admin.route('/employees')
@login_required
def list_employees():
    check_admin()

    employees = Employee.query.all()
    return render_template('admin/employee/employees.html',
                            employees=employees, title="Employés")

@admin.route('/employees/assign/<int:id>', methods=['GET','POST'])
@login_required
def assign_employee(id):

    check_admin()

    employee = Employee.query.get_or_404(id)

    if employee.is_admin:
        abort(403)
    
    form = EmployeeAssignForm(obj=employee)
    if form.validate_on_submit():
        employee.department= form.department.data
        employee.role = form.role.data
        db.session.add(employee)
        db.session.commit()
        flash("L'employée a été affecter à un département et un poste avec succès")

        return redirect(url_for('admin.list_employees'))
    return render_template('admin/employee/employee.html',
                            employee=employee, form=form,
                            title="Affecter employé")