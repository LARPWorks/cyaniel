from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


# Project Cyaniel Models

character_attributes = db.Table('character_attributes',
                                db.Column('character_id', db.Integer, db.ForeignKey('characters.id')),
                                db.Column('attribute_id', db.Integer, db.ForeignKey('attributes.id')),
                                db.Column('rank', db.Integer),
                                db.Column('last_modified', db.DateTime),
                                db.Column('comments', db.String(1024))
                                )


user_roles = db.Table("user_roles",
                      db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                      db.Column('role_id', db.Integer, db.ForeignKey('roles.id'))
                      )

"""
A requirement for an AdvancementListAttribute to be visible/valid in an advancement list.
"""
advancement_list_requirements = db.Table('advancement_list_requirements',
                                         db.Column('advancement_list_attribute_id', db.Integer,
                                                   db.ForeignKey('advancement_list_attributes.id')),
                                         db.Column('attribute_requirement_id', db.Integer,
                                                   db.ForeignKey('attributes.id')),
                                         db.Column('requirement_rank', db.Integer)
                                         )

ticket_comments = db.Table('ticket_comments',
                           db.Column('ticket_id', db.Integer, db.ForeignKey('bucket_tickets.id')),
                           db.Column('author_id', db.Integer, db.ForeignKey('users.id')),
                           db.Column('comment', db.String(1024)),
                           db.Column('created_on', db.DateTime)
                           )

ticket_access_lists = db.Table('ticket_access_lists',
                               db.Column('ticket_id', db.Integer, db.ForeignKey('bucket_tickets.id')),
                               db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                               db.Column('can_write', db.Boolean),
                               db.Column('can_read', db.Boolean)
                               )


class User(UserMixin, db.Model):
    """
    Create a User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    user_name = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    birth_month = db.Column(db.String(20))
    birth_day = db.Column(db.Integer)
    birth_year = db.Column(db.Integer)
    join_date = db.Column(db.DateTime)
    experience_points = db.Column(db.Integer)  # Refers to proprietary character build points
    game_points = db.Column(db.Integer)  # Refers to proprietary redeemable game points
    emergency_contact_name = db.Column(db.String(60))
    emergency_contact_number = db.Column(db.String(20))
    password_hash = db.Column(db.String(128), nullable=False)
    last_update = db.Column(db.DateTime)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    roles = db.relationship("Role", secondary=user_roles)
    characters = db.relationship("Character", back_populates="user")
    awards = db.relationship("AwardLog", back_populates='user')

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


class AwardLog(db.Model):
    """
    A log table that tracks various point awards to characters or users.
    
    A sample award would be experience points for a character, or glory for a player.
    """

    __tablename__ = 'award_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates='award_logs')
    # only assigned if award is character-specific
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    character = db.relationship("Character", back_populates='award_logs')
    award_type_id = db.Column(db.Integer, db.ForeignKey('award_types.id'), nullable=False)
    award_type = db.relationship("AwardType")
    award_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Integer, nullable=False, default=0)
    reason = db.Column(db.String(512))

    def __repr__(self):
        return 'Award ({0}): {1}'.format(self.award_type.name, self.amount)


class AwardType(db.Model):
    """
    A table specifying some kind of point-value award able to be granted to users or characters.
    """

    __tablename__ = 'award_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32))

    def __repr__(self):
        return '<Award Type: {}'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Character(db.Model):
    """
    Create a Player Character table - all characters assigned to user
    """

    __tablename__ = 'characters'

    id = db.Column(db.Integer, primary_key=True)
    character_name = db.Column(db.String(60), nullable=False)
    create_date = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", back_populates="characters")
    attributes = db.relationship("Attribute", secondary=character_attributes)
    awards = db.relationship("AwardLog", back_populates='character')
    items = db.relationship("Inventory", back_populates='character')
    notes = db.relationship("CharacterNotes", back_populates='character')

    def __repr__(self):
        return '<Character: {}>'.format(self.name)


class Attribute(db.Model):
    """
    Create a master index of all character related attributes (skills, etc...)
    """

    __tablename__ = 'attributes'

    id = db.Column(db.Integer, primary_key=True)
    attribute_name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(200))
    attribute_type_id = db.Column(db.Integer, db.ForeignKey('attribute_types.id'), nullable=False)
    attribute_type = db.relationship("AttributeType")

    def __repr__(self):
        return '<Attribute: {}>'.format(self.name)


class AttributeType(db.Model):
    __tablename__ = 'attribute_types'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)

    def __repr__(self):
        return '<Attribute Type: {}>'.format(self.name)


class Inventory(db.Model):
    """
    Create an Inventory table where items are tied to each character
    """

    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    character = db.relationship("Character", back_populates='items')
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    def __repr__(self):
        return '<Inventory: {}>'.format(self.name)


class Items(db.Model):
    """
    Create and Inventory table as an index for all in-game items and materials
    """

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(200), nullable=False, unique=True)
    description = db.Column(db.Text(200))
    item_attr = db.Column(db.Text(200))
    last_update = db.Column(db.DateTime)

    def __repr__(self):
        return '<Item: {}>'.format(self.name)


class CharacterNotes(db.Model):
    """
    Create a table to house mostly clob-like fields of character notes
    """

    __tablename__ = 'character_notes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text(500))
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    character = db.relationship("Character", back_populates='notes')

    def __repr__(self):
        return '<Character Note: {}>'.format(self.name)


class AdvancementList(db.Model):
    """
    A type of list for character generation / character advancement options.
    """

    __tablename__ = 'advancement_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    is_chargen_only = db.Column(db.Boolean, default=False, nullable=False)
    is_staff_only = db.Column(db.Boolean, default=False, nullable=False)
    options = db.relationship('AdvancementListAttribute')

    def __repr(self):
        return "<Advancement List: {}>".format(self.name)


class AdvancementListAttribute(db.Model):
    """
    A possible option for an advancement list, assuming all AdvancementListRequirements are met.
    """

    __tablename__ = 'advancement_list_attributes'

    id = db.Column(db.Integer, primary_key=True)
    advancement_list_id = db.Column(db.Integer, db.ForeignKey("advancement_lists.id"), nullable=False)
    advancement_list = db.relationship('AdvancementList')
    attribute_id = db.Column(db.Integer, db.ForeignKey('attributes.id'), nullable=False)
    attribute = db.relationship("Attribute")
    is_staff_only = db.Column(db.Boolean, default=False, nullable=False)
    is_free_with_requirements = db.Column(db.Boolean, default=False, nullable=False)
    requirements = db.relationship('Attribute', secondary=advancement_list_requirements)

    def __repr__(self):
        return "<Advancement List Attribute: {}>".format(self.attribute.name)


class Bucket(db.Model):
    """
    A category for tickets to live in.
    """

    __tablename__ = 'buckets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))

    def __repr__(self):
        return "<Bucket: {}>".format(self.name)


class BucketTicket(db.Model):
    """
    A ticket in the queue for staff administration,
    """

    __tablename__ = 'bucket_tickets'

    id = db.Column(db.Integer, primary_key=True)
    bucket_id = db.Column(db.Integer, db.ForeignKey('buckets.id'), nullable=False)
    bucket = db.relationship('Bucket')
    title = db.Column(db.String(128))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User')
    assignee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    assignee = db.ForeignKey('User')
    status = db.Column(db.Integer)
    created_on = db.Column(db.DateTime)
    last_modified = db.Column(db.DateTime)

    def __repr__(self):
        return "<Ticket: {}>".format(self.title)
