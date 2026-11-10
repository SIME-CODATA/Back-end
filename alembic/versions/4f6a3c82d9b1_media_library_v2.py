"""media library v2

Revision ID: 4f6a3c82d9b1
Revises: 77248e576909
Create Date: 2026-11-06
"""

from alembic import op
import sqlalchemy as sa

revision = "4f6a3c82d9b1"
down_revision = "77248e576909"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "media_assets" not in inspector.get_table_names():
        op.create_table(
            "media_assets",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(120), nullable=False),
            sa.Column("folder", sa.String(30), nullable=False),
            sa.Column("original_name", sa.String(255), nullable=False),
            sa.Column("storage_name", sa.String(255), nullable=False, unique=True),
            sa.Column("relative_path", sa.String(520), nullable=False, unique=True),
            sa.Column("media_type", sa.String(20), nullable=False),
            sa.Column("mime_type", sa.String(120), nullable=False),
            sa.Column("extension", sa.String(20), nullable=False),
            sa.Column("size_bytes", sa.Integer(), nullable=False, server_default="0"),
            sa.Column("checksum_sha256", sa.String(64), nullable=False),
            sa.Column("alt_text", sa.String(500), nullable=False, server_default=""),
            sa.Column("description", sa.String(1500), nullable=False, server_default=""),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column("created_by", sa.Integer(), nullable=True),
            sa.Column("updated_by", sa.Integer(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.UniqueConstraint("folder", "name", name="uq_media_assets_folder_name"),
        )
    else:
        columns = {c["name"] for c in inspector.get_columns("media_assets")}
        if "name" not in columns:
            op.add_column("media_assets", sa.Column("name", sa.String(120), nullable=True))
        if "folder" not in columns:
            op.add_column("media_assets", sa.Column("folder", sa.String(30), nullable=True))
        if "relative_path" not in columns:
            op.add_column("media_assets", sa.Column("relative_path", sa.String(520), nullable=True))

        op.execute("""
            UPDATE media_assets
               SET name = COALESCE(name, 'media-' || id::text),
                   folder = COALESCE(folder, 'outros'),
                   relative_path = COALESCE(relative_path, storage_name)
        """)
        op.alter_column("media_assets", "name", nullable=False)
        op.alter_column("media_assets", "folder", nullable=False)
        op.alter_column("media_assets", "relative_path", nullable=False)

        inspector = sa.inspect(bind)
        constraints = {c.get("name") for c in inspector.get_unique_constraints("media_assets")}
        if "uq_media_assets_folder_name" not in constraints:
            op.create_unique_constraint(
                "uq_media_assets_folder_name",
                "media_assets",
                ["folder", "name"],
            )

    inspector = sa.inspect(bind)
    indexes = {i["name"] for i in inspector.get_indexes("media_assets")}
    for name, cols in {
        "ix_media_assets_name": ["name"],
        "ix_media_assets_folder": ["folder"],
        "ix_media_assets_media_type": ["media_type"],
        "ix_media_assets_is_active": ["is_active"],
        "ix_media_assets_checksum_sha256": ["checksum_sha256"],
    }.items():
        if name not in indexes:
            op.create_index(name, "media_assets", cols)


def downgrade() -> None:
    op.drop_table("media_assets")
