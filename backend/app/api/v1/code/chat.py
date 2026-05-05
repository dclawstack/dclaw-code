"""Chat and code AI endpoints."""

from datetime import datetime, timezone
from uuid import UUID, uuid4

from fastapi import APIRouter

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

MOCK_MESSAGES: dict[UUID, dict] = {}


@router.post("/messages", response_model=ChatMessageResponse)
async def create_message(data: ChatMessageCreate) -> ChatMessageResponse:
    """Create a chat message."""
    now = datetime.now(timezone.utc).isoformat()
    mid = uuid4()
    record = {
        "id": mid,
        "project_id": data.project_id,
        "role": data.role,
        "content": data.content,
        "model": data.model,
        "context_code": data.context_code,
        "file_path": data.file_path,
        "created_at": now,
        "updated_at": now,
    }
    MOCK_MESSAGES[mid] = record
    return ChatMessageResponse(
        id=mid,
        project_id=data.project_id,
        role=data.role,
        content=data.content,
        model=data.model,
        context_code=data.context_code,
        file_path=data.file_path,
        created_at=now,
        updated_at=now,
    )


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
