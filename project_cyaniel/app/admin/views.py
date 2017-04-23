from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from .forms import CharacterForm, RoleForm, UserAssignForm
from .. import db
from ..models import Character, Role, User


def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)


# Character Views


@admin.route('/characters', methods=['GET', 'POST'])
@login_required
def list_characters():
    """
    List all characters
    """
    check_admin()

    characters = Character.query.all()

    return render_template('admin/characters/characters.html',
                           characters=characters, title="Characters")


@admin.route('/characters/add', methods=['GET', 'POST'])
@login_required
def add_character():
    """
    Add a characters to the database
    """
    check_admin()

    add_character = True
    sections = [
        dict(title="General"),
        dict(title="Attributes & Skills"),
        dict(title="Equipment"),
        dict(title="Foci"),
        dict(title="Perks & Flaws"),
        dict(title="Powers & Techniques"),
        dict(title="Notes")]

    form = CharacterForm()
    if form.validate_on_submit():
        character = Character(character_name=form.character_name.data,
                              user=current_user)

        try:
            # add characters to the database
            db.session.add(character)
            db.session.commit()
            flash('You have successfully added a new characters.')
        except:
            # in case characters name already exists
            flash('Error: characters name already exists.')

        # redirect to characters page
        return redirect(url_for('admin.list_characters'))

    # load characters template
    return render_template('admin/characters/character.html', action="Add",
                           add_character=add_character, form=form, sections=sections,
                           title="Add Character")


@admin.route('/characters/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_character(id):
    """
    Edit a characters
    """
    check_admin()

    add_character = False

    character = Character.query.get_or_404(id)
    form = CharacterForm(obj=character)
    if form.validate_on_submit():
        character.character_name = form.character_name.data
        character.id = form.id.data
        db.session.commit()
        flash('You have successfully edited the characters.')

        # redirect to the characters page
        return redirect(url_for('admin.list_characters'))

    form.character_name.data = character.character_name
    return render_template('admin/characters/character.html', action="Edit",
                           add_character=add_character, form=form,
                           character=character, title="Edit Character")


@admin.route('/characters/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_character(id):
    """
    Delete a characters from the database
    """
    check_admin()

    character = Character.query.get_or_404(id)
    db.session.delete(character)
    db.session.commit()
    flash('You have successfully deleted the characters.')

    # redirect to the characters page
    return redirect(url_for('admin.list_characters'))

    return render_template(title="Delete Character")


# Role Views

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

    return render_template(title="Delete Role")


#  User Views

@admin.route('/users')
@login_required
def list_users():
    """
    List all users
    """
    check_admin()

    users = User.query.all()
    return render_template('admin/users/users.html',
                           users=users, title='Users')


@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
    """
    Assign a character and a role to an employee
    """
    check_admin()

    user = User.query.get_or_404(id)

    # prevent admin from being assigned a character or role
    if user.is_admin:
        abort(403)

    form = UserAssignForm(obj=user)
    if form.validate_on_submit():
        user.character = form.character.data
        user.role = form.role.data
        db.session.add(user)
        db.session.commit()
        flash('You have successfully assigned a character and role.')

        # redirect to the roles page
        return redirect(url_for('admin.list_users'))

    return render_template('admin/users/user.html',
                           user=user, form=form,
                           title='Assign User')