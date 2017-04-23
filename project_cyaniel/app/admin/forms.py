# Imports
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

# Local Imports
from ..models import Character, Role


class CharacterForm(FlaskForm):
    """
    Form for admin to add or edit a characters
    """
    id = HiddenField('id')
    character_name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
    """
    Form for admin to assign characters and roles to employees
    """
    character = QuerySelectField(query_factory=lambda: Character.query.all(),
                                 get_label="character_name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

