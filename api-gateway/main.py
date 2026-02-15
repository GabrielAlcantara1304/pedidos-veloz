"""
API Gateway - Pedidos Veloz (stub para CI/CD)
Ponto único de entrada; apenas health e agregação de health dos backends.
"""
import os
import httpx
from fastapi import FastAPI
from contextlib import asynccontextmanager

PEDIDOS_URL = os.getenv("PEDIDOS_SERVICE_URL", "http://pedidos:8001")
PAGAMENTOS_URL = os.getenv("PAGAMENTOS_SERVICE_URL", "http://pagamentos:8002")
ESTOQUE_URL = os.getenv("ESTOQUE_SERVICE_URL", "http://estoque:8003")


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="API Gateway - Pedidos Veloz", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "api-gateway"}


@app.get("/health/backends")
async def health_backends():
    """Agrega status dos backends (demonstração de gateway)."""
    result = {}
    for name, url in [("pedidos", PEDIDOS_URL), ("pagamentos", PAGAMENTOS_URL), ("estoque", ESTOQUE_URL)]:
        try:
            async with httpx.AsyncClient() as client:
                r = await client.get(f"{url}/health", timeout=2.0)
                result[name] = r.json() if r.status_code == 200 else {"status": "error", "code": r.status_code}
        except Exception as e:
            result[name] = {"status": "unreachable", "error": str(e)}
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
