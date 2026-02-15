# Multi-stage: build enxuto e seguro (não-root, dependências mínimas)
# Stage 1 - builder
FROM python:3.12-slim as builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    gcc libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY api-gateway/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -w /wheels -r requirements.txt

# Stage 2 - runtime
FROM python:3.12-slim as runtime
WORKDIR /app

# Usuário não-root (boa prática de segurança)
RUN addgroup --system app && adduser --system --group app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

COPY api-gateway/ .
USER app

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
