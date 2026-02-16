# Pedidos Veloz

Foco em **CI/CD e orquestração**: Docker Compose, Kubernetes, pipeline e observabilidade. Os serviços são **stubs** (apenas `/health`) para demonstrar a infraestrutura sem aplicação completa.

## Arquitetura (stubs)

- **API Gateway** (8000): `/health` e `/health/backends` (agrega health dos backends).
- **Serviço de Pedidos** (8001): `/health` e `/pedidos` (lista vazia).
- **Serviço de Pagamentos** (8002): `/health`.
- **Serviço de Estoque** (8003): `/health`.

Sem banco de dados; sem lógica de negócio.

## Pré-requisitos

- Docker e Docker Compose
- (Opcional) kubectl e cluster Kubernetes para produção

## Ambiente local (Docker Compose)

Um único comando sobe toda a stack:

```bash
docker compose up -d
```

Aguarde os healthchecks (cerca de 20–40 s). A API fica em **http://localhost:8000**.

### Comandos úteis

```bash
docker compose up -d
docker compose logs -f
docker compose down
```

### Testar

```bash
curl http://localhost:8000/health
curl http://localhost:8000/health/backends
```

## Conteinerização e versionamento

- **Dockerfiles** multi-stage em cada serviço; imagens enxutas (Python slim).
- **Boas práticas**: usuário não-root, redução de camadas, dependências mínimas.
- Imagens versionadas pelo CI (tag `latest` e SHA do commit).

## Kubernetes (produção mínima)

Manifests em `k8s/`:

- Namespace, ConfigMap, Secret
- Deployments (api-gateway, pedidos, pagamentos, estoque) com readiness/liveness probes e securityContext (runAsNonRoot)
- Services (LoadBalancer no gateway, ClusterIP nos demais)
- HPA para api-gateway, pedidos e estoque

### Aplicar no cluster

**Se você usa Kubernetes local (Docker Desktop):**

1. Ative o Kubernetes em Docker Desktop: Settings → Kubernetes → Enable Kubernetes.
2. Use o contexto local: `kubectl config use-context docker-desktop`
3. Gere as imagens e aplique:
   ```bash
   docker compose build
   kubectl apply -f k8s/
   ```
   Os manifests usam as imagens locais (`pedidos-veloz-api-gateway:latest`, etc.) com `imagePullPolicy: IfNotPresent`.

**Se você usa um cluster remoto (ex.: EKS):**  
Troque o contexto (`kubectl config use-context <seu-cluster>`) e ajuste as imagens nos Deployments para o seu registry (ex.: `ghcr.io/<owner>/pedidos-veloz-api-gateway:latest`) após o CI publicar.

## CI/CD

- **GitHub Actions** (`.github/workflows/ci.yml`):
  - Lint (Ruff) e testes (pytest) em push/PR.
  - Em push em `main`/`master`: build e push das imagens para GitHub Container Registry (ghcr.io).

Secrets no pipeline: uso de `GITHUB_TOKEN` para o registry.

## Observabilidade, deploy e escala

- **Métricas**: HPA baseado em CPU; endpoints `/health` para probes.
- **Logs**: stdout (coleta via agregador no cluster).
- **Tracing**: proposta em `docs/OBSERVABILIDADE.md`.
- **Deploy**: Rolling Update. **Escala**: HPA (target 70% CPU).

## Relatório técnico e vídeo

- **Relatório teórico** (2–3 páginas): conceituação e justificativas
- **Relatório prático** (3–6 páginas): arquitetura, Docker Compose, Kubernetes, pipeline e observabilidade.
- **Vídeo pitch** (até 4 min): link no README e no PDF.

## Vídeo Pitch

*https://www.youtube.com/watch?v=VHQI_QDNR4k*

