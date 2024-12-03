"""empty message

Revision ID: 26d8ed5fd115
Revises: a24bfe639390
Create Date: 2024-12-03 01:45:23.855948

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '26d8ed5fd115'
down_revision = 'a24bfe639390'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('image_url')
        batch_op.drop_column('image_alt')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_alt', sa.VARCHAR(length=255), nullable=True))
        batch_op.add_column(sa.Column('image_url', sa.VARCHAR(length=255), nullable=True))

    # ### end Alembic commands ###
