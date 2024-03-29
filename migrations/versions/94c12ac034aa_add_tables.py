"""add tables

Revision ID: 94c12ac034aa
Revises: 
Create Date: 2021-05-11 19:59:25.434714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '94c12ac034aa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(length=128), nullable=True),
    sa.Column('question_type', sa.String(length=128), nullable=True),
    sa.Column('answer', sa.String(length=128), nullable=True),
    sa.Column('reference_value', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('questionset',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('number_of_questions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('user_type', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('about_me', sa.String(length=140), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_table_email'), 'user_table', ['email'], unique=True)
    op.create_index(op.f('ix_user_table_username'), 'user_table', ['username'], unique=True)
    op.create_table('current_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('questionset_id', sa.Integer(), nullable=True),
    sa.Column('question_number', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.ForeignKeyConstraint(['questionset_id'], ['questionset.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('option',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=True),
    sa.Column('option_value', sa.String(length=64), nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['question.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('body', sa.String(length=140), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('page', sa.String(), nullable=True),
    sa.Column('upvotes', sa.Integer(), nullable=True),
    sa.Column('downvotes', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_post_timestamp'), 'post', ['timestamp'], unique=False)
    op.create_table('score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('questionset_id', sa.Integer(), nullable=True),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('time_taken', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['questionset_id'], ['questionset.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user_table.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('score')
    op.drop_index(op.f('ix_post_timestamp'), table_name='post')
    op.drop_table('post')
    op.drop_table('option')
    op.drop_table('current_question')
    op.drop_index(op.f('ix_user_table_username'), table_name='user_table')
    op.drop_index(op.f('ix_user_table_email'), table_name='user_table')
    op.drop_table('user_table')
    op.drop_table('questionset')
    op.drop_table('question')
    # ### end Alembic commands ###
