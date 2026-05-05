"""Chat message schemas."""

from uuid import UUID

from pydantic import BaseModel, Field


class ChatMessageBase(BaseModel):
    """Base chat message fields."""

    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str = Field(..., min_length=1)
    model: str | None = Field(None, max_length=100)
    context_code: str | None = None
    file_path: str | None = Field(None, max_length=500)


class ChatMessageCreate(ChatMessageBase):
    """Schema for creating a chat message."""

    project_id: UUID | None = None


class ChatMessageResponse(ChatMessageBase):
    """Chat message response schema."""

    id: UUID
    project_id: UUID | None = None
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
