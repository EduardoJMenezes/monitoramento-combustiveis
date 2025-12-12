"""
Router para métricas e health checks
"""
from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.dependencies import get_session
from app.cache import get_redis_client
from app.middleware import get_metrics, reset_metrics
import redis

router = APIRouter(tags=["Observability"])


@router.get("/health")
def health_check(session: Session = Depends(get_session)):
    """
    Health check completo: verifica DB, Redis e retorna status
    """
    health_status = {
        "status": "healthy",
        "services": {}
    }
    
    # Verifica PostgreSQL
    try:
        session.exec(select(1)).first()
        health_status["services"]["database"] = {
            "status": "up",
            "type": "postgresql"
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["services"]["database"] = {
            "status": "down",
            "error": str(e)
        }
    
    # Verifica Redis
    try:
        client = get_redis_client()
        client.ping()
        health_status["services"]["cache"] = {
            "status": "up",
            "type": "redis"
        }
    except (redis.RedisError, redis.ConnectionError) as e:
        health_status["status"] = "degraded"
        health_status["services"]["cache"] = {
            "status": "down",
            "error": str(e)
        }
    
    return health_status


@router.get("/metrics")
def get_app_metrics():
    """
    Retorna métricas de performance da aplicação:
    - Total de requisições
    - Tempo médio por endpoint
    - Status codes
    - Cache hit rate
    """
    app_metrics = get_metrics()
    
    # Adiciona métricas do Redis
    try:
        client = get_redis_client()
        info = client.info("stats")
        
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        
        app_metrics["cache"] = {
            "hits": hits,
            "misses": misses,
            "hit_rate": round((hits / total * 100) if total > 0 else 0, 2),
            "total_keys": len(client.keys("*"))
        }
    except (redis.RedisError, redis.ConnectionError):
        app_metrics["cache"] = {"status": "unavailable"}
    
    return app_metrics


@router.post("/metrics/reset")
def reset_app_metrics():
    """
    Reseta as métricas coletadas (útil para testes)
    """
    reset_metrics()
    return {"status": "metrics reset"}
