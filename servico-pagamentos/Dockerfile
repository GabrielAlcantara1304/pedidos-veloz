# Multi-stage - Serviço de Pagamentos
FROM python:3.12-slim as builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1

COPY servico-pagamentos/requirements.txt .
RUN pip wheel --no-cache-dir --no-deps -w /wheels -r requirements.txt

FROM python:3.12-slim as runtime
WORKDIR /app

RUN addgroup --system app && adduser --system --group app

COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/* && rm -rf /wheels

COPY servico-pagamentos/ .
USER app

EXPOSE 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]
