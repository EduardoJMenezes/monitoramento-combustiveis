from sqlmodel import Session, select, func
from typing import Optional
from app.models import FuelCollection
from app.schemas import FuelCollectionRead, PaginatedResponse


def get_collections(
    session: Session,
    page: int = 1,
    page_size: int = 10,
    fuel_type: Optional[str] = None,
    city: Optional[str] = None,
    vehicle_type: Optional[str] = None
) -> PaginatedResponse:
    """
    Busca coletas com filtros opcionais e paginação.
    
    Args:
        session: Sessão do banco de dados
        page: Número da página (começa em 1)
        page_size: Quantidade de registros por página
        fuel_type: Filtro por tipo de combustível
        city: Filtro por cidade (busca parcial)
        vehicle_type: Filtro por tipo de veículo
    
    Returns:
        PaginatedResponse com total, page, page_size e data
    """
    # Construir a query base
    statement = select(FuelCollection)
    
    # Aplicar filtros se fornecidos
    if fuel_type:
        statement = statement.where(FuelCollection.fuel_type == fuel_type)
    if city:
        statement = statement.where(FuelCollection.city.ilike(f"%{city}%"))
    if vehicle_type:
        statement = statement.where(FuelCollection.vehicle_type == vehicle_type)
    
    # Contar total de registros (antes da paginação)
    count_statement = select(func.count()).select_from(statement.subquery())
    total = session.exec(count_statement).one()
    
    # Aplicar paginação
    offset = (page - 1) * page_size
    statement = statement.offset(offset).limit(page_size).order_by(FuelCollection.collection_date.desc())
    
    # Executar query
    results = session.exec(statement).all()
    
    # Converter para FuelCollectionRead
    data = [FuelCollectionRead.model_validate(r) for r in results]
    
    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        data=data
    )
