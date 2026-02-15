# Relatório Técnico - Pedidos Veloz

**Disciplina:** Cloud DevOps - Orchestrating Containers and Micro Services  
**Projeto:** Entrega contínua de uma plataforma de pedidos em microsserviços

---

## Parte Teórica (2 a 3 páginas)

### 1. Arquitetura de microserviços e papel do DevOps em ambientes cloud-native

Na arquitetura de **microserviços**, a aplicação é decomposta em **serviços independentes**, cada um com responsabilidade bem definida, deployável e escalável de forma isolada. Cada serviço expõe APIs (geralmente HTTP/REST) e pode usar tecnologias e bancos de dados distintos. Os benefícios incluem entrega mais rápida (times podem evoluir serviços em paralelo), escalabilidade granular (escala-se apenas o serviço sob carga) e maior resiliência (falha em um serviço não derruba o sistema inteiro). Os desafios são a maior complexidade operacional (rede, descoberta de serviços, consistência distribuída), necessidade de observabilidade (logs, métricas e traces entre serviços) e governança de deploy e configuração.

Em ambientes **cloud-native**, o **DevOps** atua na ponte entre desenvolvimento e operação: automação de build, teste e deploy (CI/CD), infraestrutura como código (IaC), conteinerização e orquestração (Docker, Kubernetes), e telemetria (métricas, logs, tracing). O objetivo é reduzir tempo de entrega, diminuir risco em deploys e permitir que a aplicação escale e se recupere de falhas de forma automatizada, alinhada à metodologia 12-Factor e a práticas como rolling updates e escalabilidade baseada em demanda (HPA/VPA).

### 2. Conteinerização: Docker e Kubernetes

**Conteinerização** consiste em empacotar aplicação e dependências em unidades isoladas (containers) que rodam sobre um único kernel do sistema operacional. Isso garante consistência entre desenvolvimento e produção (“funciona na minha máquina” deixa de ser problema), uso eficiente de recursos e portabilidade entre nuvens e datacenters.

**Docker** fornece o padrão de imagem (Dockerfile), runtime e formato OCI. O **Docker Compose** orquestra múltiplos containers em um único host, definindo serviços, redes, volumes e variáveis de ambiente em um arquivo YAML. É ideal para **ambiente local e desenvolvimento**: um único comando sobe a stack completa, permitindo desenvolvimento e testes integrados sem necessidade de um cluster.

**Kubernetes (K8s)** é um **orquestrador** de containers focado em **produção**: gerencia deploy, escalabilidade, rede, armazenamento, saúde (probes) e secrets em clusters (múltiplos nós). Enquanto o Docker/Compose resolve “rodar vários containers em uma máquina”, o Kubernetes resolve “rodar e operar cargas de trabalho em um cluster de forma resiliente e escalável”.

**Quando utilizar cada abordagem:** use **Docker Compose** para desenvolvimento local, homologação em um único host e simplicidade de uso. Use **Kubernetes** para produção, quando for necessário escalar horizontalmente, fazer rolling updates sem downtime, gerenciar configurações e segredos de forma centralizada e integrar com ecossistema de observabilidade e service mesh.

### 3. Fundamentação teórica

**Orquestração de containers:** o orquestrador (ex.: Kubernetes) é responsável por agendar e manter os containers em execução nos nós do cluster; gerenciar rede (descoberta de serviços, DNS interno); prover armazenamento persistente (PersistentVolumes); e monitorar a saúde dos pods (readiness e liveness probes), reiniciando ou substituindo instâncias com falha. Isso permite que a aplicação seja tratada como um conjunto de cargas de trabalho declarativas (manifests YAML) em vez de máquinas individuais.

**CI/CD em ambientes distribuídos:** em microsserviços, o pipeline deve construir, testar e publicar **cada serviço** de forma independente (build de imagens por serviço), além de validar integrações quando necessário. O pipeline típico inclui: **build** do código e da imagem Docker; **testes** (unitários, de integração, lint); **publicação** de imagens em um registry (versionadas por tag); e **deploy** no ambiente alvo (por exemplo, atualização de Deployments no Kubernetes). O uso correto de secrets no pipeline (credenciais de registry, ambientes) e gates (testes obrigatórios antes do deploy) reduz risco e garante rastreabilidade.

**Observabilidade (métricas, logs e traces):** em sistemas distribuídos, é essencial ter visibilidade para diagnóstico e SLA. **Métricas** são medidas numéricas agregadas no tempo (ex.: requisições por segundo, uso de CPU), usadas para alertas e escalabilidade automática (HPA). **Logs** são eventos gerados pelos serviços (preferencialmente em stdout, em formato estruturado) e coletados por um agregador (ex.: Loki, Elasticsearch). **Traces** registram o fluxo de uma requisição entre vários serviços (span por serviço), permitindo identificar gargalos e falhas em cadeia; ferramentas como Jaeger e OpenTelemetry implementam tracing distribuído. Os três pilares se complementam: métricas para “algo está errado”, logs para “o que aconteceu” e traces para “onde e em qual serviço”.

### 4. Justificativa das decisões arquiteturais do projeto

- **API Gateway:** ponto único de entrada HTTP; no projeto stub, agrega o health dos backends (`/health/backends`), demonstrando o padrão de roteamento.
- **Serviços separados (Pedidos, Pagamentos, Estoque):** cada um como processo independente para escalar e deploy isolado; no projeto são stubs (apenas `/health`) para foco em CI/CD.
- **Docker Compose para local e Kubernetes para produção:** Compose atende ao requisito de “um comando” e ambiente reproduzível para dev; Kubernetes atende produção com deploy declarativo, probes, ConfigMaps/Secrets, HPA e estratégia de deploy controlada.
- **Rolling Update:** atualização gradual dos pods (novos sobem antes de encerrar os antigos), garantindo disponibilidade contínua e rollback simples em caso de falha.
- **HPA baseado em CPU:** escala automática quando a carga sobe (ex.: target 70% CPU), atendendo picos de tráfego sem provisionamento manual; alinhado à previsão de campanha promocional do enunciado.

---

## Parte Prática (3 a 6 páginas)

### 1. Ambiente local com Docker Compose

O projeto utiliza **stubs** (serviços mínimos com apenas `/health`) para demonstrar a infraestrutura, sem aplicação completa. São quatro componentes: **API Gateway** (porta 8000), **Serviço de Pedidos** (8001), **Serviço de Pagamentos** (8002) e **Serviço de Estoque** (8003). Não há banco de dados nem lógica de negócio. O `docker-compose.yml` define todos os serviços, com dependências e healthchecks: o gateway depende de Pedidos (condition service_healthy), Pagamentos e Estoque. A ordem de inicialização é respeitada e o gateway só sobe quando os backends estão prontos.

**Um único comando** sobe toda a stack: `docker compose up -d`. Após os healthchecks (cerca de 30–60 segundos), a API fica disponível em **http://localhost:8000**.

**Redes:** a rede bridge `pedidos-net` é compartilhada por todos os serviços, permitindo comunicação por nome (ex.: `http://pedidos:8001`).

**Variáveis de ambiente:** as URLs dos serviços internos (PEDIDOS_SERVICE_URL, PAGAMENTOS_SERVICE_URL, ESTOQUE_SERVICE_URL) são definidas no Compose. Não há banco de dados.

**Instruções de execução:** o README contém pré-requisitos (Docker e Docker Compose), comando de subida, exemplos com `curl` (`/health`, `/health/backends`) e comandos úteis (`logs`, `down`).

### 2. Conteinerização e versionamento

Cada serviço (api-gateway, servico-pedidos, servico-pagamentos, servico-estoque) possui **Dockerfile** próprio. Os Dockerfiles seguem **multi-stage**: estágio de build (instalação de dependências, geração de wheels) e estágio de runtime (imagem enxuta com apenas o necessário para executar a aplicação), reduzindo tamanho e superfície de ataque.

**Boas práticas de segurança:** uso de imagem base **Python slim**; criação de usuário **não-root** (`adduser --system app`) e execução da aplicação com `USER app`; redução de camadas e remoção de caches (`pip no-cache`, `rm -rf /var/lib/apt/lists/*` no build).

**Versionamento das imagens:** o pipeline de CI (GitHub Actions) faz build e push das imagens no push para `main`/`master`. Cada imagem é publicada no GitHub Container Registry (ghcr.io) com duas tags: `latest` (última versão da branch) e o **SHA do commit** (ex.: `ghcr.io/owner/pedidos-veloz-api-gateway:a1b2c3d`), permitindo rastreabilidade e deploys reproduzíveis no Kubernetes.

### 3. Kubernetes – Produção mínima

Os manifests estão em `k8s/`: **namespace** dedicado; **ConfigMaps** para configurações não sensíveis (URLs de serviços, etc.) e para o script de init do banco; **Secrets** para credenciais (senha do PostgreSQL); **Deployments** para api-gateway, pedidos, pagamentos, estoque e banco, com **readiness e liveness probes** quando aplicável e **securityContext** (runAsNonRoot) para conformidade com boas práticas; **Services** (LoadBalancer no gateway, ClusterIP nos demais); **HPA** para api-gateway, pedidos e estoque (escalabilidade automática); e **PVC** para persistência do PostgreSQL.

Aplicação no cluster: `kubectl apply -f k8s/` (ou aplicação ordenada dos arquivos conforme README). As imagens nos Deployments devem ser ajustadas para o registry utilizado (ex.: ghcr.io após o CI publicar).

### 4. CI/CD

O pipeline **GitHub Actions** (`.github/workflows/ci.yml`) é acionado em push e pull request para `main`/`master`. O job **lint-and-test** executa em todo push/PR: configura Python 3.12, instala dependências de todos os serviços, executa **Ruff** (lint) e **pytest** nos serviços que possuem testes (api-gateway e servico-estoque). O job **build-and-push** roda apenas em push para `main`/`master`: faz login no GHCR com `GITHUB_TOKEN`, constrói e publica as quatro imagens (api-gateway, pedidos, pagamentos, estoque) com tags `latest` e SHA do commit, utilizando cache do GitHub para acelerar builds.

**Secrets:** o pipeline usa `secrets.GITHUB_TOKEN` para autenticação no registry; em cenários com registry externo, devem ser configurados secrets de usuário/senha no repositório.

### 5. Observabilidade, deploy e escala

**Métricas e saúde:** os serviços expõem endpoint `/health` para readiness/liveness no Kubernetes; o HPA utiliza métricas de CPU (target 70%) para escalar automaticamente os Deployments de api-gateway, pedidos e estoque.

**Logs:** os serviços escrevem logs em stdout (padrão 12-Factor); em um cluster real, um agregador (ex.: Fluent Bit, Loki) pode coletar e centralizar os logs.

**Tracing:** a proposta de tracing distribuído (OpenTelemetry/Jaeger) e detalhes de observabilidade estão documentados em `docs/OBSERVABILIDADE.md`.

**Estratégia de deploy:** Rolling Update (padrão do Kubernetes), com zero downtime: novas réplicas são criadas e só então as antigas são encerradas.

**Escalabilidade:** HPA configurado em `k8s/hpa.yaml` para os serviços stateless; justificativa e parâmetros (min/max replicas, target CPU) estão alinhados ao requisito de suportar picos de tráfego.

### 6. Infraestrutura como código (IaC)

Os manifests Kubernetes em `k8s/` constituem **IaC declarativa**: a infraestrutura de aplicação (namespace, ConfigMaps, Secrets, Deployments, Services, HPA, PVC) é versionada no repositório e aplicada de forma idempotente com `kubectl apply`. Para provisionamento do cluster e do registry em cloud (ex.: EKS, AKS, GKE), pode ser utilizado um esqueleto em **Terraform** (módulos de cluster, node pool, registry) com justificativa no relatório ou em documento anexo; o foco do projeto está na camada de aplicação (Kubernetes manifests) e no pipeline de entrega.

---

## Vídeo Pitch

- **Link do vídeo (YouTube):** *(inserir URL aqui; pode ser não listado)*
- Conteúdo: visão geral da arquitetura, demonstração do ambiente (local ou conceitual), decisões técnicas (containers, Kubernetes, CI/CD, deploy, observabilidade e escala).

---

*Exportar este relatório para PDF: Parte Teórica com 2–3 páginas; Parte Prática com 3–6 páginas. Incluir o link do vídeo no README e no PDF da entrega.*
