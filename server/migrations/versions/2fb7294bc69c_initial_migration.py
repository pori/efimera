"""Initial migration.

Revision ID: 2fb7294bc69c
Revises: 
Create Date: 2024-07-01 22:48:08.202199

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fb7294bc69c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('note',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('link',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('title', sa.String(length=512), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('image', sa.String(length=512), nullable=True),
    sa.Column('note_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('tag', sa.String(), nullable=False),
    sa.Column('note_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['note_id'], ['note.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag')
    op.drop_table('link')
    op.drop_table('note')
    # ### end Alembic commands ###
