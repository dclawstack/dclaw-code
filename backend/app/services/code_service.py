"""AI code services (mock Ollama proxy)."""

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


def count_lines(text: str) -> int:
    """Count non-empty lines."""
    return len([line for line in text.splitlines() if line.strip()])


async def code_completion(request: CodeCompletionRequest) -> CodeCompletionResponse:
    """Generate code completion from prompt."""
    prompt_lower = request.prompt.lower()

    completions = {
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
        "class": (
            'class DataProcessor:\n'
            '    """Process and transform data."""\n'
            '\n'
            '    def __init__(self, data: list[dict]) -> None:\n'
            '        self.data = data\n'
            '\n'
            '    def filter_by(self, key: str, value) -> list[dict]:\n'
            '        """Filter data by key-value pair."""\n'
            '        return [item for item in self.data if item.get(key) == value]\n'
            '\n'
            '    def transform(self, fn) -> list:\n'
            '        """Apply transformation function."""\n'
            '        return [fn(item) for item in self.data]'
        ),
        "import": (
            'import os\n'
            'import sys\n'
            'from typing import List, Dict, Optional\n'
            'from datetime import datetime, timezone\n'
            'from pathlib import Path'
        ),
        "async def": (
            'async def fetch_data(url: str) -> dict:\n'
            '    """Fetch JSON data from URL asynchronously."""\n'
            '    import httpx\n'
            '    async with httpx.AsyncClient() as client:\n'
            '        response = await client.get(url, timeout=30.0)\n'
            '        response.raise_for_status()\n'
            '        return response.json()'
        ),
    }

    completion = None
    for keyword, code in completions.items():
        if keyword in prompt_lower:
            completion = code
            break

    if completion is None:
        completion = (
            f"# TODO: Implement based on prompt:\n"
            f"# {request.prompt[:100]}\n"
            f"\n"
            f"pass  # AI completion placeholder"
        )

    return CodeCompletionResponse(
        completion=completion,
        language=request.language,
        model_used="codellama:7b-code",
        tokens_generated=len(completion.split()),
    )


async def code_refactor(request: CodeRefactorRequest) -> CodeRefactorResponse:
    """Refactor code based on goal."""
    changes = []
    refactored = request.code

    if "readability" in request.goal.lower():
        changes.append("Added type hints and docstrings")
        changes.append("Improved variable naming")
        refactored = (
            'def improved_function(data: list[dict]) -> list[dict]:\n'
            '    """Process data with improved readability."""\n'
            '    result: list[dict] = []\n'
            '    for item in data:\n'
            '        if item.get("active"):\n'
            '            processed = {**item, "processed": True}\n'
            '            result.append(processed)\n'
            '    return result'
        )
    elif "performance" in request.goal.lower():
        changes.append("Replaced loop with list comprehension")
        changes.append("Reduced memory allocations")
        refactored = (
            'def optimized_function(data: list[dict]) -> list[dict]:\n'
            '    """Optimized version using comprehensions."""\n'
            '    return [{**item, "processed": True} for item in data if item.get("active")]'
        )
    else:
        changes.append("Applied general improvements")
        refactored = request.code + "\n\n# TODO: Review and improve"

    return CodeRefactorResponse(
        original_code=request.code,
        refactored_code=refactored,
        explanation=f"Refactored to {request.goal} with {len(changes)} improvements.",
        changes_made=changes,
        language=request.language,
    )


async def code_explain(request: CodeExplainRequest) -> CodeExplainResponse:
    """Explain code at specified detail level."""
    explanations = {
        "brief": (
            "This function processes a list of dictionaries, filtering active items "
            "and returning processed results. It uses list comprehension for efficiency."
        ),
        "medium": (
            "This function iterates over a list of dictionaries (data). For each item, "
            "it checks if the 'active' key is truthy. If so, it creates a new dictionary "
            "with all original keys plus a 'processed' flag set to True. The results are "
            "collected into a new list using a list comprehension, which is more memory-efficient "
            "than a for-loop with append."
        ),
        "detailed": (
            "This function implements a data filtering and transformation pipeline:\n\n"
            "1. **Input**: Accepts `data` — a list of dictionaries representing records.\n"
            "2. **Iteration**: Uses a list comprehension to iterate over each item.\n"
            "3. **Filtering**: Checks `item.get('active')` which returns the value for key 'active' "
            "or None if missing. In Python, None and False are falsy, so only truthy values pass.\n"
            "4. **Transformation**: Creates a new dictionary using `{**item, 'processed': True}` "
            "which unpacks all key-value pairs from the original and adds/overwrites 'processed'.\n"
            "5. **Output**: Returns a new list containing only filtered and transformed items.\n\n"
            "**Key concepts**: List comprehension, dictionary unpacking, truthiness, immutability."
        ),
    }

    detail = request.detail_level if request.detail_level in explanations else "medium"

    return CodeExplainResponse(
        code=request.code,
        explanation=explanations[detail],
        key_concepts=["List comprehension", "Dictionary unpacking", "Filtering", "Immutability"],
        language=request.language,
    )


async def code_generate_tests(request: CodeGenerateTestsRequest) -> CodeGenerateTestsResponse:
    """Generate unit tests for code."""
    test_code = (
        'import pytest\n'
        'from typing import List, Dict\n'
        '\n'
        '# Tests for the provided function\n'
        '\n'
        'def test_basic_functionality():\n'
        '    """Test with standard input."""\n'
        '    data = [\n'
        '        {"id": 1, "active": True},\n'
        '        {"id": 2, "active": False},\n'
        '        {"id": 3, "active": True},\n'
        '    ]\n'
        '    result = process_data(data)\n'
        '    assert len(result) == 2\n'
        '    assert all(item["processed"] for item in result)\n'
        '\n'
        'def test_empty_list():\n'
        '    """Test with empty input."""\n'
        '    assert process_data([]) == []\n'
        '\n'
        'def test_all_inactive():\n'
        '    """Test when no items are active."""\n'
        '    data = [{"id": 1, "active": False}]\n'
        '    assert process_data(data) == []\n'
        '\n'
        'def test_missing_active_key():\n'
        '    """Test with missing active key (treated as falsy)."""\n'
        '    data = [{"id": 1}]\n'
        '    assert process_data(data) == []\n'
        '\n'
        'def test_preserves_original():\n'
        '    """Ensure original data is not modified."""\n'
        '    data = [{"id": 1, "active": True}]\n'
        '    original = data[0].copy()\n'
        '    process_data(data)\n'
        '    assert data[0] == original\n'
    )

    return CodeGenerateTestsResponse(
        original_code=request.code,
        test_code=test_code,
        framework=request.framework,
        test_cases_count=5,
    )
