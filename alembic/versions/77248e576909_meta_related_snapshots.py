"""create meta_related_snapshots

Revision ID: 77248e576909
Revises: eb0a612d517b
Create Date: 2026-10-30
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "77248e576909"
down_revision = "eb0a612d517b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "meta_related_snapshots",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("meta_id", sa.Integer(), nullable=False),
        sa.Column("smae_meta_id", sa.Integer(), nullable=True),
        sa.Column(
            "payload",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'{}'::jsonb"),
        ),
        sa.Column(
            "geo_features",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
            server_default=sa.text("'[]'::jsonb"),
        ),
        sa.Column("synced_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["meta_id"], ["metas.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_meta_related_snapshots_meta_id",
        "meta_related_snapshots",
        ["meta_id"],
        unique=True,
    )
    op.create_index(
        "ix_meta_related_snapshots_smae_meta_id",
        "meta_related_snapshots",
        ["smae_meta_id"],
        unique=False,
    )
    op.create_index(
        "ix_meta_related_snapshots_synced_at",
        "meta_related_snapshots",
        ["synced_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_meta_related_snapshots_synced_at", table_name="meta_related_snapshots")
    op.drop_index("ix_meta_related_snapshots_smae_meta_id", table_name="meta_related_snapshots")
    op.drop_index("ix_meta_related_snapshots_meta_id", table_name="meta_related_snapshots")
    op.drop_table("meta_related_snapshots")
