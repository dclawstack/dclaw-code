"""File endpoints."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.schemas.file import FileCreate, FileResponse

router = APIRouter()

MOCK_FILES: dict[UUID, dict] = {}


def _to_response(f: dict) -> FileResponse:
    return FileResponse(
        id=f["id"],
        project_id=f["project_id"],
        path=f["path"],
        content=f.get("content"),
        language=f.get("language"),
        size_bytes=f.get("size_bytes", 0),
        line_count=f.get("line_count", 0),
        git_status=f.get("git_status"),
        created_at=f["created_at"],
        updated_at=f["updated_at"],
    )


@router.get("", response_model=list[FileResponse])
async def list_files(project_id: UUID | None = None) -> list[FileResponse]:
    """List files with optional project filter."""
    files = list(MOCK_FILES.values())
    if project_id:
        files = [f for f in files if f["project_id"] == project_id]
    return [_to_response(f) for f in files]


@router.post("", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def create_file(data: FileCreate) -> FileResponse:
    """Create a new file record."""
    now = datetime.now(timezone.utc).isoformat()
    fid = uuid4()
    content = data.content or ""
    record = {
        "id": fid,
        "project_id": data.project_id,
        "path": data.path,
        "content": content,
        "language": data.language,
        "size_bytes": len(content.encode("utf-8")),
        "line_count": content.count("\n") + 1,
        "git_status": data.git_status or "added",
        "created_at": now,
        "updated_at": now,
    }
    MOCK_FILES[fid] = record
    return _to_response(record)
