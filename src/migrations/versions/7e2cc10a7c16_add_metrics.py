"""add metrics

Revision ID: 7e2cc10a7c16
Revises: c612151d55c5
Create Date: 2024-06-17 16:22:36.399345

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7e2cc10a7c16'
down_revision: Union[str, None] = 'c612151d55c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('global_metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alltime_words_amount', sa.Integer(), nullable=True),
    sa.Column('alltime_userwords_amount', sa.Integer(), nullable=True),
    sa.Column('today_words_amount', sa.Integer(), nullable=True),
    sa.Column('today_userwords_amount', sa.Integer(), nullable=True),
    sa.Column('alltime_learned_amount', sa.Integer(), nullable=True),
    sa.Column('alltime_learned_percents', sa.Float(), nullable=True),
    sa.Column('today_learned_amount', sa.Integer(), nullable=True),
    sa.Column('today_learned_percents', sa.Float(), nullable=True),
    sa.Column('alltime_speech_seconds', sa.Integer(), nullable=True),
    sa.Column('alltime_video_seconds', sa.Integer(), nullable=True),
    sa.Column('today_speech_seconds', sa.Integer(), nullable=True),
    sa.Column('today_video_seconds', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_global_metric_id'), 'global_metric', ['id'], unique=False)
    op.create_table('user_metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('alltime_userwords_amount', sa.Integer(), nullable=True),
    sa.Column('today_words_amount', sa.Integer(), nullable=True),
    sa.Column('today_userwords_amount', sa.Integer(), nullable=True),
    sa.Column('alltime_learned_amount', sa.Integer(), nullable=True),
    sa.Column('alltime_learned_percents', sa.Float(), nullable=True),
    sa.Column('today_learned_amount', sa.Integer(), nullable=True),
    sa.Column('today_learned_percents', sa.Float(), nullable=True),
    sa.Column('alltime_speech_seconds', sa.Integer(), nullable=True),
    sa.Column('alltime_video_seconds', sa.Integer(), nullable=True),
    sa.Column('today_speech_seconds', sa.Integer(), nullable=True),
    sa.Column('today_video_seconds', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.String(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_metric_id'), 'user_metric', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_metric_id'), table_name='user_metric')
    op.drop_table('user_metric')
    op.drop_index(op.f('ix_global_metric_id'), table_name='global_metric')
    op.drop_table('global_metric')
    # ### end Alembic commands ###
