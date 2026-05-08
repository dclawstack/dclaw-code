"""File repository."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.file import File
from app.schemas.file import FileCreate, FileUpdate


class FileRepository:
    """File data access repository."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self, project_id: UUID | None = None) -> list[File]:
        """List files with optional project filter."""
        stmt = select(File).order_by(File.created_at.desc())
        if project_id:
            stmt = stmt.where(File.project_id == project_id)
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, file_id: UUID) -> File | None:
        """Get a file by ID."""
        result = await self.db.execute(select(File).where(File.id == file_id))
        return result.scalar_one_or_none()

    async def create(self, data: FileCreate) -> File:
        """Create a new file record."""
        content = data.content or ""
        file = File(
            project_id=data.project_id,
            path=data.path,
            content=content,
            language=data.language,
            size_bytes=len(content.encode("utf-8")),
            line_count=content.count("\n") + 1,
            git_status=data.git_status or "added",
        )
        self.db.add(file)
        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def update(self, file: File, data: FileUpdate) -> File:
        """Update a file."""
        if data.path is not None:
            file.path = data.path
        if data.content is not None:
            file.content = data.content
            file.size_bytes = len(data.content.encode("utf-8"))
            file.line_count = data.content.count("\n") + 1
        if data.language is not None:
            file.language = data.language
        if data.git_status is not None:
            file.git_status = data.git_status

        await self.db.commit()
        await self.db.refresh(file)
        return file

    async def delete(self, file: File) -> None:
        """Delete a file."""
        await self.db.delete(file)
        await self.db.commit()
