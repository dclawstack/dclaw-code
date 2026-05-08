"""Snippet repository."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.snippet import Snippet
from app.schemas.snippet import SnippetCreate, SnippetUpdate


class SnippetRepository:
    """Snippet data access repository."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self, project_id: UUID | None = None) -> list[Snippet]:
        """List snippets with optional project filter."""
        stmt = select(Snippet).order_by(Snippet.created_at.desc())
        if project_id:
            stmt = stmt.where(Snippet.project_id == project_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, snippet_id: UUID) -> Snippet | None:
        """Get a snippet by ID."""
        result = await self.db.execute(select(Snippet).where(Snippet.id == snippet_id))
        return result.scalar_one_or_none()

    async def create(self, data: SnippetCreate) -> Snippet:
        """Create a new snippet."""
        snippet = Snippet(
            project_id=data.project_id,
            title=data.title,
            content=data.content,
            language=data.language,
            tags=data.tags,
            line_start=data.line_start,
            line_end=data.line_end,
        )
        self.db.add(snippet)
        await self.db.commit()
        await self.db.refresh(snippet)
        return snippet

    async def update(self, snippet: Snippet, data: SnippetUpdate) -> Snippet:
        """Update a snippet."""
        if data.title is not None:
            snippet.title = data.title
        if data.content is not None:
            snippet.content = data.content
        if data.language is not None:
            snippet.language = data.language
        if data.tags is not None:
            snippet.tags = data.tags
        if data.line_start is not None:
            snippet.line_start = data.line_start
        if data.line_end is not None:
            snippet.line_end = data.line_end

        await self.db.commit()
        await self.db.refresh(snippet)
        return snippet

    async def delete(self, snippet: Snippet) -> None:
        """Delete a snippet."""
        await self.db.delete(snippet)
        await self.db.commit()
