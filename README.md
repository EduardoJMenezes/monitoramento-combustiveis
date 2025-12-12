# V-Lab - Sistema de Monitoramento de Combustíveis

Sistema Full Stack para monitoramento de vendas e preços de combustíveis em tempo real.

## 🛠️ Stack

**Backend:**
- Python + FastAPI
- PostgreSQL
- Redis (cache)
- SQLModel (ORM)
- Pytest (testes unitários)

**Frontend:**
- Next.js + TypeScript
- TailwindCSS + shadcn/ui
- React Query

**Infraestrutura:**
- Docker + Docker Compose

## ⚙️ Pré-requisitos

- **Docker Desktop** instalado e rodando
  - Windows: [Docker Desktop para Windows](https://docs.docker.com/desktop/install/windows-install/)
  - Mac: [Docker Desktop para Mac](https://docs.docker.com/desktop/install/mac-install/)
  - Linux: [Docker Engine](https://docs.docker.com/engine/install/)
- **Git** (para clonar o repositório)
- **Portas livres:** 3000 (frontend), 8000 (backend), 5432 (postgres), 6379 (redis)

## 🚀 Quick Start

```bash
# Clone e acesse o diretório
git clone <repo>
cd "Projeto V-Lab - Monitoramento de Combustíveis"

# Suba os containers (primeira vez pode demorar ~2min)
docker-compose up -d

# Verifique se todos os 4 containers estão rodando
docker ps

# Aguarde ~10s para os serviços iniciarem, então acesse:
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
# Dashboard: http://localhost:3000
```

**⚠️ Troubleshooting:**
```bash
# Se der erro de porta em uso, pare outros serviços:
# Windows: netstat -ano | findstr :8000
# Linux/Mac: lsof -i :8000

# Ver logs se algo não funcionar:
docker-compose logs backend
docker-compose logs frontend
```

## 📥 Popular o Banco com Dados Fake

O script `ingest_script/seed.py` gera e envia dados fictícios para a API:

```bash
# Opção 1: Com Python local (requer Python 3.11+)
cd ingest_script
pip install -r requirements.txt
python seed.py

# Opção 2: Usando Docker (sem instalar dependências) - RECOMENDADO
# Windows (PowerShell):
docker run --rm --network host -v "${PWD}/ingest_script:/app" -w /app python:3.11-slim bash -c "pip install -q -r requirements.txt && python seed.py"

# Linux/Mac:
docker run --rm --network host -v "$PWD/ingest_script:/app" -w /app python:3.11-slim bash -c "pip install -q -r requirements.txt && python seed.py"
```

O script gera **100 registros** fictícios e envia para `http://localhost:8000/ingest`.

**Sucesso esperado:** `✅ 100 registros inseridos com sucesso!`

## 📊 Endpoints Principais

### Ingestão de Dados
```bash
POST /ingest
```
Recebe dados de vendas (posto, combustível, motorista, veículo).

### Consultas
```bash
GET /collections?page=1&page_size=20&fuel_type=Gasolina&city=São%20Paulo
```
Listagem paginada com filtros (combustível, cidade, tipo de veículo).

### KPIs
```bash
GET /kpis/avg-price-by-fuel        # Preço médio por combustível
GET /kpis/volume-by-vehicle        # Volume total por tipo de veículo
```

### Relatórios
```bash
GET /reports/driver?cpf=12345678901
GET /reports/driver?name=João
```
Relatório de motorista com total gasto, volume e combustível favorito.

### Observabilidade
```bash
GET /health                        # Status de DB e Redis
GET /metrics                       # Métricas de performance e cache
## 🧪 Testes

```bash
# Rodar testes unitários
docker exec fastapi_api pytest tests/ -v

# Com cobertura (71% atual)
docker exec fastapi_api pytest --cov=app --cov-report=html

# Ver relatório HTML
# Windows:
start backend/htmlcov/index.html
# Mac:
open backend/htmlcov/index.html
# Linux:
xdg-open backend/htmlcov/index.html
```

**Cobertura atual:** 71% (services 100%, models 100%, schemas 94%+)

## ⚡ Features

- ✅ API RESTful com FastAPI
- ✅ Validação de dados (CPF, enums, preços)
- ✅ Paginação e filtros avançados
- ✅ Mascaramento de CPF (privacidade)
- ✅ Cache Redis nos KPIs (10min TTL)
- ✅ Invalidação automática de cache
- ✅ Health checks (DB + Redis)
- ✅ Métricas de performance
- ✅ Testes unitários (pytest)
- ✅ Arquitetura em camadas (routers → services → models)

## 📁 Estrutura do Projeto

```
.
├── backend/
│   ├── app/
│   │   ├── routers/        # Endpoints HTTP
│   │   ├── services/       # Lógica de negócio
│   │   ├── models/         # Modelos SQLModel
│   │   ├── schemas/        # Schemas Pydantic
│   │   ├── cache.py        # Redis utilities
│   │   ├── database.py     # Conexão DB
│   │   ├── middleware.py   # Métricas
│   │   └── dependencies.py # Injeção de dependências
│   ├── tests/          # Testes unitários
│   ├── main.py         # Entry point
│   └── requirements.txt
├── frontend/
│   ├── app/            # Next.js App Router
│   ├── components/     # React components
│   └── lib/            # API client, utils
├── ingest_script/
│   └── seed.py        # Gerador de dados fake
└── docker-compose.yml
```

## 🔧 Comandos Úteis

```bash
# Ver logs
docker-compose logs -f backend

# Acessar container do backend
docker exec -it fastapi_api bash

# Limpar cache do Redis
curl -X DELETE http://localhost:8000/cache/clear

## 📌 Variáveis de Ambiente

As variáveis já estão configuradas no `docker-compose.yml`. Não precisa criar arquivo `.env` para rodar localmente.

```env
# Backend (já configurado)
DATABASE_URL=postgresql://user_vlab:password_vlab@db/fuel_monitor_db
REDIS_URL=redis://redis:6379/0
UVICORN_PORT=8000
```

## 🎯 Testando a API

Exemplos práticos com `curl`:

```bash
# 1. Health check
curl http://localhost:8000/health

# 2. Listar coletas (após rodar seed.py)
curl "http://localhost:8000/collections?page=1&page_size=5"

# 3. KPI de preço médio
curl http://localhost:8000/kpis/avg-price-by-fuel

# 4. Buscar motorista por CPF
curl "http://localhost:8000/reports/driver?cpf=12345678901"

# 5. Métricas do sistema
curl http://localhost:8000/metrics
```

Ou use a **documentação interativa** em http://localhost:8000/docs

---

**Desenvolvido com FastAPI + Next.js**
```env
DATABASE_URL=postgresql://user:pass@db/dbname
REDIS_URL=redis://redis:6379/0
UVICORN_PORT=8000
```

---
