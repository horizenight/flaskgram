"""fixing

Revision ID: 040398632d4c
Revises: 6c874b840e59
Create Date: 2022-12-30 12:53:23.969557

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '040398632d4c'
down_revision = '6c874b840e59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.String(length=120), nullable=False))
        batch_op.create_unique_constraint(None, ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='unique')
        batch_op.drop_column('username')

    # ### end Alembic commands ###
