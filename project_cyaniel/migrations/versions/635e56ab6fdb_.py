"""empty message

Revision ID: 635e56ab6fdb
Revises: 
Create Date: 2017-04-07 01:58:44.165560

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '635e56ab6fdb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('advancement_lists',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('is_chargen_only', sa.Boolean(), nullable=True),
    sa.Column('is_staff_only', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('attribute_types',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(length=200), nullable=True),
    sa.Column('description', sa.Text(length=200), nullable=True),
    sa.Column('item_attr', sa.Text(length=200), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_items_item_name'), 'items', ['item_name'], unique=True)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=60), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('user_name', sa.String(length=200), nullable=True),
    sa.Column('first_name', sa.String(length=60), nullable=True),
    sa.Column('last_name', sa.String(length=60), nullable=True),
    sa.Column('birth_month', sa.String(length=20), nullable=True),
    sa.Column('birth_day', sa.Integer(), nullable=True),
    sa.Column('birth_year', sa.Integer(), nullable=True),
    sa.Column('join_date', sa.DateTime(), nullable=True),
    sa.Column('experience_points', sa.Integer(), nullable=True),
    sa.Column('game_points', sa.Integer(), nullable=True),
    sa.Column('emergency_contact_name', sa.String(length=60), nullable=True),
    sa.Column('emergency_contact_number', sa.String(length=20), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_birth_day'), 'users', ['birth_day'], unique=False)
    op.create_index(op.f('ix_users_birth_month'), 'users', ['birth_month'], unique=False)
    op.create_index(op.f('ix_users_birth_year'), 'users', ['birth_year'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_join_date'), 'users', ['join_date'], unique=False)
    op.create_table('attributes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('attribute_name', sa.String(length=200), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.Column('attribute_type_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attribute_type_id'], ['attribute_types.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('attribute_name')
    )
    op.create_table('characters',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('character_name', sa.String(length=60), nullable=True),
    sa.Column('create_date', sa.DateTime(), nullable=True),
    sa.Column('last_update', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_characters_character_name'), 'characters', ['character_name'], unique=False)
    op.create_table('experience_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('award_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_roles',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    op.create_table('advancement_list_attributes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('advancement_list_id', sa.Integer(), nullable=True),
    sa.Column('attribute_id', sa.Integer(), nullable=True),
    sa.Column('is_staff_only', sa.Boolean(), nullable=True),
    sa.Column('is_free_with_requirements', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['advancement_list_id'], ['advancement_lists.id'], ),
    sa.ForeignKeyConstraint(['attribute_id'], ['attributes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('character_attributes',
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('attribute_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['attribute_id'], ['attributes.id'], ),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], )
    )
    op.create_table('character_notes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('body', sa.Text(length=500), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('character_id', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_inventory_quantity'), 'inventory', ['quantity'], unique=False)
    op.create_table('advancement_list_requirements',
    sa.Column('advancement_list_attribute_id', sa.Integer(), nullable=True),
    sa.Column('attribute_requirement_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['advancement_list_attribute_id'], ['advancement_list_attributes.id'], ),
    sa.ForeignKeyConstraint(['attribute_requirement_id'], ['attributes.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('advancement_list_requirements')
    op.drop_index(op.f('ix_inventory_quantity'), table_name='inventory')
    op.drop_table('inventory')
    op.drop_table('character_notes')
    op.drop_table('character_attributes')
    op.drop_table('advancement_list_attributes')
    op.drop_table('user_roles')
    op.drop_table('experience_logs')
    op.drop_index(op.f('ix_characters_character_name'), table_name='characters')
    op.drop_table('characters')
    op.drop_table('attributes')
    op.drop_index(op.f('ix_users_join_date'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_birth_year'), table_name='users')
    op.drop_index(op.f('ix_users_birth_month'), table_name='users')
    op.drop_index(op.f('ix_users_birth_day'), table_name='users')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_index(op.f('ix_items_item_name'), table_name='items')
    op.drop_table('items')
    op.drop_table('attribute_types')
    op.drop_table('advancement_lists')
    # ### end Alembic commands ###
