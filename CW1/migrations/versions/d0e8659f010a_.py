"""empty message

Revision ID: d0e8659f010a
Revises: 
Create Date: 2024-10-29 14:50:25.639833

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0e8659f010a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('assessment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('module_code', sa.String(length=100), nullable=False),
    sa.Column('deadline', sa.DateTime(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('assessment')
    # ### end Alembic commands ###
