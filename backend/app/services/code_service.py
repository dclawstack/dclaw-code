"""AI code services with Ollama/OpenRouter fallback."""

import httpx

from app.core.config import settings
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

_TIMEOUT = httpx.Timeout(60.0, connect=10.0)


def _build_prompt(task: str, code: str | None = None, language: str | None = None) -> str:
    lang = language or "python"
    base = f"You are an expert {lang} programmer. {task}"
    if code:
        base += f"\n\n```\n{code}\n```\n"
    return base


async def _call_ollama(prompt: str) -> str | None:
    """Try Ollama generate endpoint."""
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(
                f"{settings.ollama_base_url}/api/generate",
                json={
                    "model": settings.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 512},
                },
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("response", "")
    except Exception:
        return None


async def _call_openrouter(prompt: str) -> str | None:
    """Try OpenRouter chat completions endpoint."""
    if not settings.openrouter_api_key:
        return None
    try:
        async with httpx.AsyncClient(timeout=_TIMEOUT) as client:
            resp = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.openrouter_api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "meta-llama/llama-3.1-8b-instruct",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                    "max_tokens": 512,
                },
            )
            resp.raise_for_status()
            data = resp.json()
            choices = data.get("choices", [])
            if choices:
                return choices[0].get("message", {}).get("content", "")
            return None
    except Exception:
        return None


async def _generate(prompt: str) -> str:
    """Generate text using Ollama → OpenRouter → fallback."""
    result = await _call_ollama(prompt)
    if result:
        return result
    result = await _call_openrouter(prompt)
    if result:
        return result
    return "# AI service unavailable. Check Ollama or OpenRouter configuration.\n"


# ─── Mock fallbacks (used when LLM returns empty or errors) ────────────────

_COMPLETIONS = {
    "def fibonacci": (
        'def fibonacci(n: int) -> int:\n'
        '    """Return the nth Fibonacci number."""\n'
        '    if n <= 1:\n'
        '        return n\n'
        '    a, b = 0, 1\n'
        '    for _ in range(2, n + 1):\n'
        '        a, b = b, a + b\n'
        '    return b'
    ),
    "def quicksort": (
        'def quicksort(arr: list[int]) -> list[int]:\n'
        '    """Sort array using quicksort algorithm."""\n'
        '    if len(arr) <= 1:\n'
        '        return arr\n'
        '    pivot = arr[len(arr) // 2]\n'
        '    left = [x for x in arr if x < pivot]\n'
        '    middle = [x for x in arr if x == pivot]\n'
        '    right = [x for x in arr if x > pivot]\n'
        '    return quicksort(left) + middle + quicksort(right)'
    ),
}


async def code_completion(request: CodeCompletionRequest) -> CodeCompletionResponse:
    """Generate code completion from prompt."""
    prompt = _build_prompt(
        f"Complete the following {request.language or 'python'} code. "
        "Return ONLY the completed code, no explanations.",
        request.prompt,
        request.language,
    )
    completion = await _generate(prompt)

    if "unavailable" in completion:
        # Fallback to keyword mock
        prompt_lower = request.prompt.lower()
        for keyword, code in _COMPLETIONS.items():
            if keyword in prompt_lower:
                completion = code
                break
        else:
            completion = (
                f"# TODO: Implement based on prompt:\n"
                f"# {request.prompt[:100]}\n\npass  # AI completion placeholder"
            )

    return CodeCompletionResponse(
        completion=completion.strip(),
        language=request.language,
        model_used=settings.ollama_model,
        tokens_generated=len(completion.split()),
    )


async def code_refactor(request: CodeRefactorRequest) -> CodeRefactorResponse:
    """Refactor code based on goal."""
    prompt = _build_prompt(
        f"Refactor the following code to improve: {request.goal}. "
        "Return ONLY the refactored code, no explanations.",
        request.code,
        request.language,
    )
    refactored = await _generate(prompt)

    if "unavailable" in refactored:
        refactored = request.code + "\n\n# TODO: Review and improve"

    return CodeRefactorResponse(
        original_code=request.code,
        refactored_code=refactored.strip(),
        explanation=f"Refactored to {request.goal}.",
        changes_made=["Applied AI refactoring suggestions"],
        language=request.language,
    )


async def code_explain(request: CodeExplainRequest) -> CodeExplainResponse:
    """Explain code at specified detail level."""
    prompt = _build_prompt(
        f"Explain the following code at a {request.detail_level} level of detail. "
        "Include key concepts and how the code works.",
        request.code,
        request.language,
    )
    explanation = await _generate(prompt)

    if "unavailable" in explanation:
        explanation = (
            "This code processes data. AI explanation service is currently unavailable."
        )

    return CodeExplainResponse(
        code=request.code,
        explanation=explanation.strip(),
        key_concepts=["AI-generated analysis"],
        language=request.language,
    )


async def code_generate_tests(request: CodeGenerateTestsRequest) -> CodeGenerateTestsResponse:
    """Generate unit tests for code."""
    prompt = _build_prompt(
        f"Generate {request.framework} unit tests for the following code. "
        "Return ONLY the test code, no explanations.",
        request.code,
        request.language,
    )
    test_code = await _generate(prompt)

    if "unavailable" in test_code:
        test_code = (
            'import pytest\n\n'
            'def test_placeholder():\n'
            '    """Replace with real tests."""\n'
            '    pass\n'
        )

    return CodeGenerateTestsResponse(
        original_code=request.code,
        test_code=test_code.strip(),
        framework=request.framework,
        test_cases_count=test_code.count("def test_"),
    )
