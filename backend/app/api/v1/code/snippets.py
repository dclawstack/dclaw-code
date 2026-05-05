"""Snippet endpoints."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.schemas.snippet import SnippetCreate, SnippetResponse

router = APIRouter()

MOCK_SNIPPETS: dict[UUID, dict] = {}


def _to_response(s: dict) -> SnippetResponse:
    return SnippetResponse(
        id=s["id"],
        project_id=s["project_id"],
        title=s["title"],
        content=s["content"],
        language=s.get("language"),
        tags=s.get("tags"),
        line_start=s.get("line_start"),
        line_end=s.get("line_end"),
        created_at=s["created_at"],
        updated_at=s["updated_at"],
    )


@router.get("", response_model=list[SnippetResponse])
async def list_snippets(project_id: UUID | None = None) -> list[SnippetResponse]:
    """List snippets with optional project filter."""
    snippets = list(MOCK_SNIPPETS.values())
    if project_id:
        snippets = [s for s in snippets if s["project_id"] == project_id]
    return [_to_response(s) for s in snippets]


@router.post("", response_model=SnippetResponse, status_code=status.HTTP_201_CREATED)
async def create_snippet(data: SnippetCreate) -> SnippetResponse:
    """Create a new snippet."""
    now = datetime.now(timezone.utc).isoformat()
    sid = uuid4()
    record = {
        "id": sid,
        "project_id": data.project_id,
        "title": data.title,
        "content": data.content,
        "language": data.language,
        "tags": data.tags,
        "line_start": data.line_start,
        "line_end": data.line_end,
        "created_at": now,
        "updated_at": now,
    }
    MOCK_SNIPPETS[sid] = record
    return _to_response(record)
