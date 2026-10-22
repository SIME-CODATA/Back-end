from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


class CmsPage(SQLModel, table=True):
    """Página administrável do site público."""

    __tablename__ = "cms_pages"

    id: int | None = Field(
        default=None,
        primary_key=True,
    )

    key: str = Field(
        max_length=80,
        unique=True,
        index=True,
    )

    title: str = Field(
        max_length=160,
    )

    description: str = Field(
        default="",
        max_length=500,
    )

    is_active: bool = Field(
        default=True,
        index=True,
    )

    created_at: datetime = Field(
        default_factory=_utc_now,
        index=True,
    )

    updated_at: datetime = Field(
        default_factory=_utc_now,
        index=True,
    )
