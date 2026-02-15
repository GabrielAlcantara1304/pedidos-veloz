# Observabilidade - Pedidos Veloz

## Métricas
- **Kubernetes**: HPA utiliza métricas de CPU (metrics-server) para escalar api-gateway, pedidos e estoque.
- **Aplicação**: Cada serviço expõe endpoint `/health` para readiness/liveness. Para produção, recomenda-se expor métricas no formato Prometheus (ex.: `prometheus_client` em Python) em `/metrics`.

## Logs
- Logs são enviados para stdout/stderr (12-Factor). Em Kubernetes, use um sidecar ou daemonset (Fluent Bit, Filebeat) para coletar e enviar para um agregador (Elasticsearch, Loki).

## Tracing distribuído
- Proposta: instrumentar com **OpenTelemetry** (SDK Python) e exportar para Jaeger ou Tempo. Cada requisição receberia um `trace_id` propagado via headers (ex.: `traceparent` W3C).
- Service mesh (Istio) oferece tracing automático com Jaeger; alternativa mais leve é instrumentação manual nas aplicações.

## Estratégia de deploy
- **Rolling Update** configurado nos Deployments: `maxSurge: 1`, `maxUnavailable: 0`, garantindo disponibilidade durante o deploy.

## Escalabilidade
- **HPA** (Horizontal Pod Autoscaler) para api-gateway, pedidos e estoque, com target de CPU 70%, min/max réplicas definidos nos manifests em `k8s/hpa.yaml`.
