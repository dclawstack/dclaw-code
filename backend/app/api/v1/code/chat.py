"""Chat and code AI endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.chat_repo import ChatMessageRepository
from app.schemas.chat_message import ChatMessageCreate, ChatMessageResponse
from app.schemas.code import (
    CodeCompletionRequest,
    CodeCompletionResponse,
    CodeExplainRequest,
    CodeExplainResponse,
    CodeGenerateTestsRequest,
    CodeGenerateTestsResponse,
    CodeRefactorRequest,
    CodeRefactorResponse,
)
from app.services.code_service import (
    code_completion,
    code_explain,
    code_generate_tests,
    code_refactor,
)

router = APIRouter()


@router.get("/messages", response_model=list[ChatMessageResponse])
async def list_messages(
    project_id: UUID | None = None,
    db: AsyncSession = Depends(get_db),
) -> list[ChatMessageResponse]:
    """List chat messages with optional project filter."""
    repo = ChatMessageRepository(db)
    messages = await repo.list_all(project_id=project_id)
    return [ChatMessageResponse.model_validate(m) for m in messages]


@router.post("/messages", response_model=ChatMessageResponse)
async def create_message(
    data: ChatMessageCreate,
    db: AsyncSession = Depends(get_db),
) -> ChatMessageResponse:
    """Create a chat message."""
    repo = ChatMessageRepository(db)
    message = await repo.create(data)
    return ChatMessageResponse.model_validate(message)


@router.post("/completion", response_model=CodeCompletionResponse)
async def completion(request: CodeCompletionRequest) -> CodeCompletionResponse:
    """AI code completion."""
    return await code_completion(request)


@router.post("/refactor", response_model=CodeRefactorResponse)
async def refactor(request: CodeRefactorRequest) -> CodeRefactorResponse:
    """Code refactoring suggestions."""
    return await code_refactor(request)


@router.post("/explain", response_model=CodeExplainResponse)
async def explain(request: CodeExplainRequest) -> CodeExplainResponse:
    """Explain selected code."""
    return await code_explain(request)


@router.post("/generate-tests", response_model=CodeGenerateTestsResponse)
async def generate_tests(request: CodeGenerateTestsRequest) -> CodeGenerateTestsResponse:
    """Generate unit tests."""
    return await code_generate_tests(request)
