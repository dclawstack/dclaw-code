"""Snippet endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.snippet_repo import SnippetRepository
from app.schemas.snippet import SnippetCreate, SnippetResponse, SnippetUpdate

router = APIRouter()


@router.get("", response_model=list[SnippetResponse])
async def list_snippets(
    project_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[SnippetResponse]:
    """List snippets with optional project filter."""
    repo = SnippetRepository(db)
    snippets = await repo.list_all(project_id=project_id)
    return [SnippetResponse.model_validate(s) for s in snippets]


@router.post("", response_model=SnippetResponse, status_code=status.HTTP_201_CREATED)
async def create_snippet(
    data: SnippetCreate,
    db: AsyncSession = Depends(get_db),
) -> SnippetResponse:
    """Create a new snippet."""
    repo = SnippetRepository(db)
    snippet = await repo.create(data)
    return SnippetResponse.model_validate(snippet)


@router.get("/{snippet_id}", response_model=SnippetResponse)
async def get_snippet(
    snippet_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> SnippetResponse:
    """Get a snippet by ID."""
    repo = SnippetRepository(db)
    snippet = await repo.get_by_id(snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return SnippetResponse.model_validate(snippet)


@router.put("/{snippet_id}", response_model=SnippetResponse)
async def update_snippet(
    snippet_id: UUID,
    data: SnippetUpdate,
    db: AsyncSession = Depends(get_db),
) -> SnippetResponse:
    """Update a snippet."""
    repo = SnippetRepository(db)
    snippet = await repo.get_by_id(snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    snippet = await repo.update(snippet, data)
    return SnippetResponse.model_validate(snippet)


@router.delete("/{snippet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_snippet(
    snippet_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete a snippet."""
    repo = SnippetRepository(db)
    snippet = await repo.get_by_id(snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    await repo.delete(snippet)
