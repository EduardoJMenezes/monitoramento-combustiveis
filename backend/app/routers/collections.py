from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional

from app.dependencies import get_session
from app.schemas import PaginatedResponse
from app.services.collection_service import get_collections as get_collections_service

router = APIRouter(prefix="/collections", tags=["Consultas"])


@router.get("", response_model=PaginatedResponse)
def get_collections(
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    fuel_type: Optional[str] = Query(None, description="Filtrar por tipo de combustível"),
    city: Optional[str] = Query(None, description="Filtrar por cidade"),
    vehicle_type: Optional[str] = Query(None, description="Filtrar por tipo de veículo"),
    session: Session = Depends(get_session)
):
    """
    Retorna listagem paginada de coletas com filtros opcionais.
    
    Filtros disponíveis:
    - fuel_type: Gasolina, Etanol, Diesel S10
    - city: Nome da cidade
    - vehicle_type: Carro, Moto, Caminhão Leve, Carreta, Ônibus
    """
    return get_collections_service(
        session=session,
        page=page,
        page_size=page_size,
        fuel_type=fuel_type,
        city=city,
        vehicle_type=vehicle_type
    )
