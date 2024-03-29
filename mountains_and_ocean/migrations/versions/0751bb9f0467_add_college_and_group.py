"""add college and group

Revision ID: 0751bb9f0467
Revises: c5a9edd264f3
Create Date: 2019-09-03 11:09:40.714953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0751bb9f0467'
down_revision = 'c5a9edd264f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('college',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('image', sa.String(length=280), nullable=False),
    sa.Column('site', sa.Integer(), nullable=False),
    sa.Column('intro', sa.String(length=680), nullable=True),
    sa.Column('level', sa.Enum('初级', '二级', '一级', 'Z级'), nullable=True),
    sa.ForeignKeyConstraint(['site'], ['site.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('group',
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('update_time', sa.DateTime(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('image', sa.String(length=280), nullable=False),
    sa.Column('site', sa.Integer(), nullable=False),
    sa.Column('intro', sa.String(length=680), nullable=True),
    sa.Column('level', sa.Enum('初级', '二级', '一级', 'Z级'), nullable=True),
    sa.ForeignKeyConstraint(['site'], ['site.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('role', sa.Column('college', sa.Integer(), nullable=True))
    op.add_column('role', sa.Column('group', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'role', 'group', ['group'], ['id'])
    op.create_foreign_key(None, 'role', 'college', ['college'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'role', type_='foreignkey')
    op.drop_constraint(None, 'role', type_='foreignkey')
    op.drop_column('role', 'group')
    op.drop_column('role', 'college')
    op.drop_table('group')
    op.drop_table('college')
    # ### end Alembic commands ###
