"""blog class

Revision ID: 558f0673aad9
Revises: f6a2548b804f
Create Date: 2022-02-18 07:14:37.247050

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '558f0673aad9'
down_revision = 'f6a2548b804f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('blogs', sa.String(length=5000), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blogs')
    # ### end Alembic commands ###