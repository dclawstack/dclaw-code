"""Chat message repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chat_message import ChatMessage
from app.schemas.chat_message import ChatMessageCreate


class ChatMessageRepository:
    """Chat message data access repository."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self, project_id: UUID | None = None) -> list[ChatMessage]:
        """List chat messages with optional project filter."""
        stmt = select(ChatMessage).order_by(ChatMessage.created_at.asc())
        if project_id:
            stmt = stmt.where(ChatMessage.project_id == project_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create(self, data: ChatMessageCreate) -> ChatMessage:
        """Create a new chat message."""
        message = ChatMessage(
            project_id=data.project_id,
            role=data.role,
            content=data.content,
            model=data.model,
            context_code=data.context_code,
            file_path=data.file_path,
        )
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message
