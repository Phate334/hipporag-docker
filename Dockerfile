FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=0 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
ENV UV_HTTP_TIMEOUT=300
ENV UV_CONCURRENT_DOWNLOADS=1

WORKDIR /app

# Install dependencies with retry logic and cleanup
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    for i in {1..3}; do \
        uv sync --locked --no-install-project --no-dev && break || \
        (echo "Attempt $i failed, retrying in 30 seconds..." && sleep 30); \
    done && \
    # Clean up unnecessary files to reduce layer size
    find /app/.venv -name "*.pyc" -delete && \
    find /app/.venv -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -name "*.pyo" -delete

FROM python:3.12-slim-bookworm

# Create non-root user for security
RUN groupadd -r app && useradd -r -g app app

# Copy only the virtual environment from builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app

# Switch to non-root user
USER app

ENTRYPOINT ["/app/.venv/bin/python"]