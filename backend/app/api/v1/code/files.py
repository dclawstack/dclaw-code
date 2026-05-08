"""File endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.file_repo import FileRepository
from app.schemas.file import FileCreate, FileResponse, FileUpdate

router = APIRouter()


@router.get("", response_model=list[FileResponse])
async def list_files(
    project_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[FileResponse]:
    """List files with optional project filter."""
    repo = FileRepository(db)
    files = await repo.list_all(project_id=project_id)
    return [FileResponse.model_validate(f) for f in files]


@router.post("", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def create_file(
    data: FileCreate,
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """Create a new file record."""
    repo = FileRepository(db)
    file = await repo.create(data)
    return FileResponse.model_validate(file)


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """Get a file by ID."""
    repo = FileRepository(db)
    file = await repo.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse.model_validate(file)


@router.put("/{file_id}", response_model=FileResponse)
async def update_file(
    file_id: UUID,
    data: FileUpdate,
    db: AsyncSession = Depends(get_db),
) -> FileResponse:
    """Update a file."""
    repo = FileRepository(db)
    file = await repo.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file = await repo.update(file, data)
    return FileResponse.model_validate(file)


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a file."""
    repo = FileRepository(db)
    file = await repo.get_by_id(file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    await repo.delete(file)
