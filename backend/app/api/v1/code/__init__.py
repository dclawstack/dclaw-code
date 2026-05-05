"""Aggregate code API routers."""

from fastapi import APIRouter

from app.api.v1.code import chat, files, projects, snippets

router = APIRouter()
router.include_router(projects.router, prefix="/projects", tags=["Projects"])
router.include_router(files.router, prefix="/files", tags=["Files"])
router.include_router(snippets.router, prefix="/snippets", tags=["Snippets"])
router.include_router(chat.router, prefix="/chat", tags=["Chat"])
