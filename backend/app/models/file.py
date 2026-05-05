"""Code file model."""

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class File(Base, UUIDMixin, TimestampMixin):
    """Source code file."""

    __tablename__ = "files"

    project_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    path: Mapped[str] = mapped_column(String(500), nullable=False)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    size_bytes: Mapped[int] = mapped_column(default=0)
    line_count: Mapped[int] = mapped_column(default=0)
    git_status: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )  # modified / added / deleted / clean

    project: Mapped["Project"] = relationship("Project", back_populates="files")
