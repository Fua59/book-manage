"""empty message

Revision ID: 069a0eae6214
Revises: 86d391e3cda0
Create Date: 2024-12-30 18:25:35.785281

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '069a0eae6214'
down_revision = '86d391e3cda0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'types', ['booktype_id'], ['id'])

    with op.batch_alter_table('borrows', schema=None) as batch_op:
        batch_op.create_foreign_key(None, 'users', ['user_id'], ['id'])
        batch_op.create_foreign_key(None, 'books', ['book_id'], ['id'])
        batch_op.drop_column('borrow_time')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('borrows', schema=None) as batch_op:
        batch_op.add_column(sa.Column('borrow_time', mysql.DATETIME(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.drop_constraint(None, type_='foreignkey')

    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')

    # ### end Alembic commands ###