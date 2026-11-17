# Node >= 22.22.0 é exigido pela versão atual do Reflex.
FROM node:22.22.0-bookworm-slim AS node
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    REFLEX_USE_NPM=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl unzip libstdc++6 libatomic1 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=node /usr/local/bin/node /usr/local/bin/node
COPY --from=node /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx \
    && node --version \
    && npm --version

RUN pip install --no-cache-dir uv
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY . .
RUN uv sync --frozen --no-dev \
    && chmod +x /app/docker-entrypoint.backend.sh

EXPOSE 3000
ENTRYPOINT ["/app/docker-entrypoint.sh"]
