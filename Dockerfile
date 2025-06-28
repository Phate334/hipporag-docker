FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=0 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0
ENV UV_HTTP_TIMEOUT=300
ENV UV_CONCURRENT_DOWNLOADS=1

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    for i in {1..3}; do \
        uv sync --locked --no-install-project --no-dev && break || \
        (echo "Attempt $i failed, retrying in 30 seconds..." && sleep 30); \
    done

FROM python:3.12-slim-bookworm
COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app

ENTRYPOINT ["/app/.venv/bin/python"]