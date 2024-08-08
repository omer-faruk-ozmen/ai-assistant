"""Result nullable true

Revision ID: 981a12e9100a
Revises: 58eefb81af92
Create Date: 2024-07-04 16:51:55.932815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '981a12e9100a'
down_revision = '58eefb81af92'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('conclusions', schema=None) as batch_op:
        batch_op.alter_column('result',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('conclusions', schema=None) as batch_op:
        batch_op.alter_column('result',
               existing_type=sa.TEXT(),
               nullable=False)

    # ### end Alembic commands ###
