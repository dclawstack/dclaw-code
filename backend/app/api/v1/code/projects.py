"""Project endpoints."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter, HTTPException, status

from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate

router = APIRouter()

MOCK_PROJECTS: dict[UUID, dict] = {}


def _to_response(p: dict) -> ProjectResponse:
    return ProjectResponse(
        id=p["id"],
        name=p["name"],
        description=p.get("description"),
        language=p.get("language"),
        repo_url=p.get("repo_url"),
        git_branch=p.get("git_branch", "main"),
        settings=p.get("settings"),
        created_at=p["created_at"],
        updated_at=p["updated_at"],
    )


@router.get("", response_model=list[ProjectResponse])
async def list_projects() -> list[ProjectResponse]:
    """List all projects."""
    return [_to_response(p) for p in MOCK_PROJECTS.values()]


@router.post("", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate) -> ProjectResponse:
    """Create a new project."""
    now = datetime.now(timezone.utc).isoformat()
    pid = uuid4()
    record = {
        "id": pid,
        "name": data.name,
        "description": data.description,
        "language": data.language,
        "repo_url": data.repo_url,
        "git_branch": data.git_branch,
        "settings": data.settings,
        "created_at": now,
        "updated_at": now,
    }
    MOCK_PROJECTS[pid] = record
    return _to_response(record)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID) -> ProjectResponse:
    """Get a project by ID."""
    p = MOCK_PROJECTS.get(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    return _to_response(p)


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: UUID, data: ProjectUpdate) -> ProjectResponse:
    """Update a project."""
    p = MOCK_PROJECTS.get(project_id)
    if not p:
        raise HTTPException(status_code=404, detail="Project not found")
    for field in ["name", "description", "language", "repo_url", "git_branch", "settings"]:
        val = getattr(data, field)
        if val is not None:
            p[field] = val
    p["updated_at"] = datetime.now(timezone.utc).isoformat()
    return _to_response(p)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: UUID) -> None:
    """Delete a project."""
    if project_id not in MOCK_PROJECTS:
        raise HTTPException(status_code=404, detail="Project not found")
    del MOCK_PROJECTS[project_id]
