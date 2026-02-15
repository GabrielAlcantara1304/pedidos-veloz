# Multi-stage - Serviço de Pedidos
FROM python:3.12-slim as builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

RUN apt-get update -qq && apt-get install -y --no-install-recommends \
    gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY servico-pedidos/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -w /wheels -r requirements.txt

FROM python:3.12-slim as runtime
WORKDIR /app

RUN addgroup --system app && adduser --system --group app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

COPY servico-pedidos/ .
USER app

EXPOSE 8001
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
