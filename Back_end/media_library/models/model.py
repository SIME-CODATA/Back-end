from datetime import datetime, timezone

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MediaAsset(SQLModel, table=True):
    __tablename__ = "media_assets"
    __table_args__ = (
        UniqueConstraint("folder", "name", name="uq_media_assets_folder_name"),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=120, index=True)
    folder: str = Field(max_length=30, index=True)

    original_name: str = Field(max_length=255, index=True)
    storage_name: str = Field(max_length=255, unique=True, index=True)
    relative_path: str = Field(max_length=520, unique=True)

    media_type: str = Field(max_length=20, index=True)
    mime_type: str = Field(max_length=120)
    extension: str = Field(max_length=20)

    size_bytes: int = Field(default=0)
    checksum_sha256: str = Field(max_length=64, index=True)

    alt_text: str = Field(default="", max_length=500)
    description: str = Field(default="", max_length=1500)

    is_active: bool = Field(default=True, index=True)
    created_by: int | None = Field(default=None, index=True)
    updated_by: int | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=_utc_now, index=True)
    updated_at: datetime = Field(default_factory=_utc_now, index=True)
