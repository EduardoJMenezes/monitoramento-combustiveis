"""
Redis cache configuration and utilities
"""
import redis
import json
import os
from typing import Optional, Any
from functools import wraps


# Configuração do Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Cliente Redis global
redis_client: Optional[redis.Redis] = None


def get_redis_client() -> redis.Redis:
    """
    Obtém o cliente Redis (singleton pattern)
    """
    global redis_client
    if redis_client is None:
        redis_client = redis.from_url(
            REDIS_URL,
            decode_responses=True,  # Retorna strings ao invés de bytes
            socket_connect_timeout=5,
            socket_timeout=5
        )
    return redis_client


def cache_key(*args, **kwargs) -> str:
    """
    Gera uma chave de cache única baseada nos argumentos
    """
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}:{v}" for k, v in sorted(kwargs.items())])
    return ":".join(key_parts)


def cached(prefix: str, ttl: int = 300, skip_args: int = 0):
    """
    Decorator para cachear resultado de funções
    
    Args:
        prefix: Prefixo da chave no Redis (ex: "kpi:avg_price")
        ttl: Tempo de vida do cache em segundos (padrão: 5 minutos)
        skip_args: Número de argumentos a ignorar na chave (ex: session)
    
    Exemplo:
        @cached("kpi:avg_price", ttl=600, skip_args=1)  # Ignora primeiro arg (session)
        def get_avg_price_by_fuel(session):
            ...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # Remove os primeiros argumentos (geralmente session)
                cache_args = args[skip_args:]
                
                # Gera chave única
                key = f"{prefix}:{cache_key(*cache_args, **kwargs)}"
                
                # Tenta buscar do cache
                client = get_redis_client()
                cached_value = client.get(key)
                
                if cached_value is not None:
                    # Cache hit - retorna valor deserializado
                    return json.loads(cached_value)
                
                # Cache miss - executa função
                result = func(*args, **kwargs)
                
                # Converte para dict se for lista de Pydantic models
                serializable_result = result
                if isinstance(result, list) and len(result) > 0:
                    if hasattr(result[0], 'model_dump'):
                        serializable_result = [item.model_dump() for item in result]
                elif hasattr(result, 'model_dump'):
                    serializable_result = result.model_dump()
                
                # Salva no cache
                client.setex(
                    key,
                    ttl,
                    json.dumps(serializable_result, default=str)
                )
                
                return result
                
            except (redis.RedisError, redis.ConnectionError) as e:
                # Se Redis falhar, executa função normalmente
                print(f"Redis error: {e}")
                return func(*args, **kwargs)
        
        return wrapper
    return decorator


def invalidate_cache(pattern: str):
    """
    Invalida chaves de cache que correspondem ao padrão
    
    Args:
        pattern: Padrão de chave (ex: "kpi:*" invalida todos os KPIs)
    """
    try:
        client = get_redis_client()
        keys = client.keys(pattern)
        if keys:
            client.delete(*keys)
    except (redis.RedisError, redis.ConnectionError) as e:
        print(f"Redis error on invalidation: {e}")
