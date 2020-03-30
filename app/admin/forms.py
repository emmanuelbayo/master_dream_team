from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField

from .. models import Department,Role

class DepartementForm(FlaskForm):
    """
    Formulaire pour ajouter ou éditer un departement

    """
    name = StringField('Nom', validators=[DataRequired()])
    description = StringField('Description',validators=[DataRequired()])
    submit = SubmitField('Créer')

class RoleForm(FlaskForm):
    name = StringField('Nom',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Soumettre')

class EmployeeAssignForm(FlaskForm):
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                    get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Appliquer')