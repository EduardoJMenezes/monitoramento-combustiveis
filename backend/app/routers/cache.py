"""
Router para monitoramento e debug do cache Redis
"""
from fastapi import APIRouter
from app.cache import get_redis_client, invalidate_cache
import redis

router = APIRouter(prefix="/cache", tags=["Cache"])


@router.get("/health")
def check_redis_health():
    """
    Verifica se o Redis está conectado e funcionando
    """
    try:
        client = get_redis_client()
        client.ping()
        return {
            "status": "connected",
            "message": "Redis is healthy"
        }
    except (redis.RedisError, redis.ConnectionError) as e:
        return {
            "status": "disconnected",
            "message": f"Redis error: {str(e)}"
        }


@router.get("/stats")
def get_cache_stats():
    """
    Retorna estatísticas do cache
    """
    try:
        client = get_redis_client()
        info = client.info("stats")
        
        return {
            "total_connections_received": info.get("total_connections_received"),
            "total_commands_processed": info.get("total_commands_processed"),
            "keyspace_hits": info.get("keyspace_hits", 0),
            "keyspace_misses": info.get("keyspace_misses", 0),
            "hit_rate": round(
                info.get("keyspace_hits", 0) / 
                max(info.get("keyspace_hits", 0) + info.get("keyspace_misses", 0), 1) * 100, 
                2
            )
        }
    except (redis.RedisError, redis.ConnectionError) as e:
        return {"error": str(e)}


@router.get("/keys")
def list_cache_keys():
    """
    Lista todas as chaves armazenadas no cache
    """
    try:
        client = get_redis_client()
        keys = client.keys("*")
        
        result = {}
        for key in keys:
            ttl = client.ttl(key)
            result[key] = {
                "ttl_seconds": ttl,
                "expires_in": f"{ttl // 60}min {ttl % 60}s" if ttl > 0 else "expired/no expiry"
            }
        
        return {
            "total_keys": len(keys),
            "keys": result
        }
    except (redis.RedisError, redis.ConnectionError) as e:
        return {"error": str(e)}


@router.delete("/clear")
def clear_cache(pattern: str = "*"):
    """
    Limpa as chaves do cache que correspondem ao padrão
    
    Args:
        pattern: Padrão de chave (default: "*" limpa tudo)
                 Exemplos: "kpi:*", "kpi:avg_price:*"
    """
    try:
        invalidate_cache(pattern)
        return {
            "status": "success",
            "message": f"Cache cleared for pattern: {pattern}"
        }
    except (redis.RedisError, redis.ConnectionError) as e:
        return {"error": str(e)}
