# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy app code BEFORE installing (for hatchling to find packages)
COPY . .

# Install Python package
RUN pip install --no-cache-dir -e ".[dev]"

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8094

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8094/health')" || exit 1

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8094"]
