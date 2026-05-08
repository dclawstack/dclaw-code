"""File schemas."""

from uuid import UUID

from pydantic import BaseModel, Field


class FileBase(BaseModel):
    """Base file fields."""

    path: str = Field(..., min_length=1, max_length=500)
    content: str | None = None
    language: str | None = Field(None, max_length=50)
    size_bytes: int = 0
    line_count: int = 0
    git_status: str | None = Field(None, max_length=20)


class FileCreate(FileBase):
    """Schema for creating a file."""

    project_id: UUID


class FileUpdate(BaseModel):
    """Schema for updating a file."""

    path: str | None = Field(None, min_length=1, max_length=500)
    content: str | None = None
    language: str | None = Field(None, max_length=50)
    git_status: str | None = Field(None, max_length=20)


class FileResponse(FileBase):
    """File response schema."""

    id: UUID
    project_id: UUID
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
