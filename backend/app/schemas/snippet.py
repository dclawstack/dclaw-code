"""Snippet schemas."""

from uuid import UUID

from pydantic import BaseModel, Field


class SnippetBase(BaseModel):
    """Base snippet fields."""

    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    language: str | None = Field(None, max_length=50)
    tags: str | None = Field(None, max_length=255)
    line_start: int | None = None
    line_end: int | None = None


class SnippetCreate(SnippetBase):
    """Schema for creating a snippet."""

    project_id: UUID


class SnippetResponse(SnippetBase):
    """Snippet response schema."""

    id: UUID
    project_id: UUID
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
