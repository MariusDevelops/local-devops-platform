FROM python:3.12-slim AS base
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
WORKDIR /app
COPY pyproject.toml uv.lock ./

FROM base AS test
RUN uv sync --frozen
COPY main.py test_main.py ./
CMD ["uv", "run", "pytest"]

FROM base AS final
RUN uv sync --frozen --no-dev
COPY main.py .
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]