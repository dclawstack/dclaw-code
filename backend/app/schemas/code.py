"""Code operation schemas."""

from pydantic import BaseModel, Field


class CodeCompletionRequest(BaseModel):
    """Request for AI code completion."""

    prompt: str = Field(..., min_length=1, description="Code prompt or partial code")
    language: str = Field(default="python", max_length=50)
    max_tokens: int = Field(default=256, ge=1, le=2048)
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    context: str | None = Field(None, description="Additional code context")


class CodeCompletionResponse(BaseModel):
    """Response with code completion."""

    completion: str
    language: str
    model_used: str
    tokens_generated: int
    disclaimer: str = "AI-generated code. Review before use in production."


class CodeRefactorRequest(BaseModel):
    """Request for code refactoring."""

    code: str = Field(..., min_length=1, description="Code to refactor")
    language: str = Field(default="python", max_length=50)
    goal: str = Field(
        default="improve readability",
        description="Refactoring goal: improve readability, optimize performance, add type hints, etc."
    )


class CodeRefactorResponse(BaseModel):
    """Response with refactored code."""

    original_code: str
    refactored_code: str
    explanation: str
    changes_made: list[str]
    language: str
    disclaimer: str = "Review refactored code before committing."


class CodeExplainRequest(BaseModel):
    """Request for code explanation."""

    code: str = Field(..., min_length=1, description="Code to explain")
    language: str = Field(default="python", max_length=50)
    detail_level: str = Field(default="medium", pattern="^(brief|medium|detailed)$")


class CodeExplainResponse(BaseModel):
    """Response with code explanation."""

    code: str
    explanation: str
    key_concepts: list[str]
    language: str


class CodeGenerateTestsRequest(BaseModel):
    """Request to generate unit tests."""

    code: str = Field(..., min_length=1, description="Code to generate tests for")
    language: str = Field(default="python", max_length=50)
    framework: str = Field(default="pytest", max_length=50)
    coverage_target: str = Field(default="happy path + edge cases", max_length=100)


class CodeGenerateTestsResponse(BaseModel):
    """Response with generated tests."""

    original_code: str
    test_code: str
    framework: str
    test_cases_count: int
    disclaimer: str = "Run generated tests to verify correctness before relying on them."
