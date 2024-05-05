"""Add missing columns

Revision ID: 4d60e60c8ccf
Revises: 
Create Date: 2024-05-05 01:52:55.181481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4d60e60c8ccf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('user')
    # op.add_column('uploaded_file', sa.Column('user_id', sa.Integer(), nullable=False))
    # op.alter_column('uploaded_file', 'type',
    #            existing_type=sa.VARCHAR(length=255),
    #            nullable=True)
    # op.alter_column('uploaded_file', 'size',
    #            existing_type=sa.INTEGER(),
    #            nullable=True)
    # op.alter_column('uploaded_file', 'path',
    #            existing_type=sa.VARCHAR(length=255),
    #            nullable=True)
    # op.create_foreign_key(None, 'uploaded_file', 'users', ['user_id'], ['id'])

    # new upgrade
    op.add_column('uploaded_file', sa.Column('user_id', sa.Integer(), nullable=True))
    op.execute('UPDATE uploaded_file SET user_id = (SELECT min(id) FROM users)')  # Example update, adjust as needed
    op.alter_column('uploaded_file', 'user_id', nullable=False)  # Now set it to not nullable after all rows have a user_id
    op.alter_column('uploaded_file', 'type', existing_type=sa.VARCHAR(length=255), nullable=True)
    op.alter_column('uploaded_file', 'size', existing_type=sa.INTEGER(), nullable=True)
    op.alter_column('uploaded_file', 'path', existing_type=sa.VARCHAR(length=255), nullable=True)
    op.create_foreign_key(None, 'uploaded_file', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'uploaded_file', type_='foreignkey')
    # op.alter_column('uploaded_file', 'path',
    #            existing_type=sa.VARCHAR(length=255),
    #            nullable=False)
    # op.alter_column('uploaded_file', 'size',
    #            existing_type=sa.INTEGER(),
    #            nullable=False)
    # op.alter_column('uploaded_file', 'type',
    #            existing_type=sa.VARCHAR(length=255),
    #            nullable=False)
    # op.drop_column('uploaded_file', 'user_id')
    # op.create_table('user',
    # sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    # sa.Column('username', sa.VARCHAR(length=80), autoincrement=False, nullable=False),
    # sa.Column('password_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True),
    # sa.PrimaryKeyConstraint('id', name='user_pkey'),
    # sa.UniqueConstraint('username', name='user_username_key')
    # )

    # new downgrade
    op.drop_constraint(None, 'uploaded_file', type_='foreignkey')
    op.alter_column('uploaded_file', 'path', existing_type=sa.VARCHAR(length=255), nullable=False)
    op.alter_column('uploaded_file', 'size', existing_type=sa.INTEGER(), nullable=False)
    op.alter_column('uploaded_file', 'type', existing_type=sa.VARCHAR(length=255), nullable=False)
    op.drop_column('uploaded_file', 'user_id')
    # ### end Alembic commands ###
