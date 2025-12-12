from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Importar módulos internos
from app.database import create_db_and_tables
from app.routers import ingest, collections, kpis, reports, cache, observability
from app.middleware import MetricsMiddleware

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    Roda ao inicializar e encerrar o FastAPI.
    """
    logger.info("Iniciando aplicação e criando tabelas...")
    create_db_and_tables()
    yield
    logger.info("Encerrando aplicação...")


# Criação da aplicação FastAPI
app = FastAPI(
    title="V-Lab Fuel Monitor API",
    description="API para monitoramento de combustíveis do Ministério dos Transportes",
    version="1.0.0",
    lifespan=lifespan
)

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware de métricas
app.add_middleware(MetricsMiddleware)

# Incluir os roteadores
app.include_router(observability.router)
app.include_router(ingest.router)
app.include_router(collections.router)
app.include_router(kpis.router)
app.include_router(reports.router)
app.include_router(cache.router)


@app.get("/")
def read_root():
    """Endpoint de health check"""
    return {
        "status": "running",
        "service": "V-Lab Fuel Monitor API",
        "version": "1.0.0"
    }
