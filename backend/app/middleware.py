"""
Middleware para métricas e observabilidade
"""
import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict
from typing import Dict

logger = logging.getLogger(__name__)

# Armazena métricas em memória
metrics: Dict[str, dict] = {
    "requests": defaultdict(lambda: {"count": 0, "total_time": 0, "avg_time": 0}),
    "status_codes": defaultdict(int),
    "total_requests": 0
}


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Middleware que captura tempo de resposta e métricas por endpoint
    """
    
    async def dispatch(self, request: Request, call_next):
        # Ignora métricas próprias para não criar loop
        if request.url.path == "/metrics":
            return await call_next(request)
        
        start_time = time.time()
        
        # Processa requisição
        response = await call_next(request)
        
        # Calcula tempo de resposta
        process_time = time.time() - start_time
        
        # Atualiza métricas
        path = request.url.path
        method = request.method
        endpoint_key = f"{method} {path}"
        
        metrics["requests"][endpoint_key]["count"] += 1
        metrics["requests"][endpoint_key]["total_time"] += process_time
        metrics["requests"][endpoint_key]["avg_time"] = (
            metrics["requests"][endpoint_key]["total_time"] / 
            metrics["requests"][endpoint_key]["count"]
        )
        
        metrics["status_codes"][response.status_code] += 1
        metrics["total_requests"] += 1
        
        # Adiciona header com tempo de processamento
        response.headers["X-Process-Time"] = f"{process_time:.4f}"
        
        # Log de requisições lentas (> 1s)
        if process_time > 1.0:
            logger.warning(
                f"Slow request: {method} {path} - {process_time:.2f}s - Status: {response.status_code}"
            )
        
        return response


def get_metrics() -> dict:
    """
    Retorna as métricas coletadas
    """
    return {
        "total_requests": metrics["total_requests"],
        "endpoints": dict(metrics["requests"]),
        "status_codes": dict(metrics["status_codes"])
    }


def reset_metrics():
    """
    Reseta as métricas
    """
    metrics["requests"].clear()
    metrics["status_codes"].clear()
    metrics["total_requests"] = 0
