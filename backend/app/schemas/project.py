"""Project schemas."""

from datetime import date
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ProjectBase(BaseModel):
    """Base project fields."""

    name: str = Field(..., min_length=1, max_length=255)
    description: str | None = None
    language: str | None = Field(None, max_length=50)
    repo_url: str | None = Field(None, max_length=500)
    git_branch: str = Field(default="main", max_length=100)
    settings: dict[str, Any] | None = None


class ProjectCreate(ProjectBase):
    """Schema for creating a project."""


class ProjectUpdate(BaseModel):
    """Schema for updating a project."""

    name: str | None = None
    description: str | None = None
    language: str | None = None
    repo_url: str | None = None
    git_branch: str | None = None
    settings: dict[str, Any] | None = None


class ProjectResponse(ProjectBase):
    """Project response schema."""

    id: UUID
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
