# syntax=docker/dockerfile:1

# Vueの成果物を作る。ツール版はルートmise.tomlと揃える。
FROM node:24.22.2-bookworm-slim AS frontend-build
WORKDIR /build/projects/app/frontend
RUN npm install --global pnpm@12.15.0
COPY projects/app/frontend/package.json projects/app/frontend/pnpm-lock.yaml projects/app/frontend/pnpm-workspace.yaml ./
RUN --mount=type=cache,target=/root/.local/share/pnpm/store pnpm install --frozen-lockfile
COPY projects/app/frontend/ ./
RUN pnpm build

# 相対参照を保ち、coreを含む本番依存を非editableで導入する。
FROM python:3.14.10-slim-bookworm AS backend-build
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /usr/local/bin/uv
ENV UV_PROJECT_ENVIRONMENT=/opt/venv UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=never
WORKDIR /build/projects/app/backend
COPY projects/core/ /build/projects/core/
COPY projects/app/backend/ ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev --no-editable

# 実行環境へPython環境とVueのdistだけを渡す。Node.js・uvは含めない。
FROM python:3.14.10-slim-bookworm AS runtime
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STATIC_DIR=/app/frontend \
    HOME=/app
RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /app app
COPY --from=backend-build /opt/venv /opt/venv
COPY --from=frontend-build /build/projects/app/frontend/dist /app/frontend
USER app
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=5 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3)"]
CMD ["python", "-m", "uvicorn", "app_base_backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
