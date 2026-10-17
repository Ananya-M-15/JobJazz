"""add roadmap table

Revision ID: 5b813be1bb86
Revises: 38f89b1b139a
Create Date: 2026-10-17 00:00:56.562020

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b813be1bb86'
down_revision: Union[str, Sequence[str], None] = '38f89b1b139a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from sqlalchemy.dialects import postgresql


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'roadmaps',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('analysis_id', sa.UUID(), nullable=False),
        sa.Column('preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('summary', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('modules', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('schedule', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['analysis_id'], ['analyses.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roadmaps_analysis_id'), 'roadmaps', ['analysis_id'], unique=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_roadmaps_analysis_id'), table_name='roadmaps')
    op.drop_table('roadmaps')
