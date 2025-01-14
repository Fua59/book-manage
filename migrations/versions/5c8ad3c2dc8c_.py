"""empty message

Revision ID: 5c8ad3c2dc8c
Revises: df8710b81b44
Create Date: 2024-12-28 23:49:19.369197

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5c8ad3c2dc8c'
down_revision = 'df8710b81b44'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'types', ['booktype_id'], ['id'])

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('privilege',
               existing_type=mysql.INTEGER(display_width=11),
               type_=sa.Boolean(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('privilege',
               existing_type=sa.Boolean(),
               type_=mysql.INTEGER(display_width=11),
               existing_nullable=False)

    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###
