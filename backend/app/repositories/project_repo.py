"""Project repository."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectRepository:
    """Project data access repository."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def list_all(self) -> list[Project]:
        """List all projects."""
        result = await self.db.execute(select(Project).order_by(Project.created_at.desc()))
        return list(result.scalars().all())

    async def get_by_id(self, project_id: UUID) -> Project | None:
        """Get a project by ID."""
        result = await self.db.execute(
            select(Project).where(Project.id == project_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: ProjectCreate) -> Project:
        """Create a new project."""
        project = Project(
            name=data.name,
            description=data.description,
            language=data.language,
            repo_url=data.repo_url,
            git_branch=data.git_branch,
            settings=data.settings,
        )
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def update(self, project: Project, data: ProjectUpdate) -> Project:
        """Update a project."""
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        if data.language is not None:
            project.language = data.language
        if data.repo_url is not None:
            project.repo_url = data.repo_url
        if data.git_branch is not None:
            project.git_branch = data.git_branch
        if data.settings is not None:
            project.settings = data.settings

        await self.db.commit()
        await self.db.refresh(project)
        return project

    async def delete(self, project: Project) -> None:
        """Delete a project."""
        await self.db.delete(project)
        await self.db.commit()

    async def count(self) -> int:
        """Count total projects."""
        result = await self.db.execute(select(func.count()).select_from(Project))
        return result.scalar() or 0
