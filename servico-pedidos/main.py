"""
Serviço de Pedidos - Pedidos Veloz (stub para CI/CD)
Apenas health; sem persistência.
"""
from fastapi import FastAPI
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="Serviço de Pedidos", version="1.0.0", lifespan=lifespan)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "pedidos"}


@app.get("/pedidos")
async def listar_pedidos():
    """Stub: lista vazia (sem aplicação)."""
    return []


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
