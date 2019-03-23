"""empty message

Revision ID: 74e3aaf9724b
Revises: 2b3ba89210ce
Create Date: 2019-03-23 12:00:20.087621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74e3aaf9724b'
down_revision = '2b3ba89210ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ad',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=True),
    sa.Column('content', sa.String(length=512), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_ad_timestamp'), 'ad', ['timestamp'], unique=False)
    op.drop_index('ix_ads_timestamp', table_name='ads')
    op.drop_table('ads')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ads',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('title', sa.VARCHAR(length=64), nullable=True),
    sa.Column('content', sa.VARCHAR(length=512), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_ads_timestamp', 'ads', ['timestamp'], unique=False)
    op.drop_index(op.f('ix_ad_timestamp'), table_name='ad')
    op.drop_table('ad')
    # ### end Alembic commands ###