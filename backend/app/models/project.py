"""Project model."""

import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.file import File
    from app.models.snippet import Snippet


class Project(Base, UUIDMixin, TimestampMixin):
    """Code project repository."""

    __tablename__ = "projects"

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    language: Mapped[str | None] = mapped_column(String(50), nullable=True)
    repo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    git_branch: Mapped[str | None] = mapped_column(String(100), nullable=True, default="main")
    settings: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    files: Mapped[list["File"]] = relationship(
        "File", back_populates="project", lazy="selectin", cascade="all, delete-orphan"
    )
    snippets: Mapped[list["Snippet"]] = relationship(
        "Snippet", back_populates="project", lazy="selectin", cascade="all, delete-orphan"
    )
