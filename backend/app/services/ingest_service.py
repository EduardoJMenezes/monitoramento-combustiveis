from sqlmodel import Session
from app.models import FuelCollection
from app.schemas import FuelCollectionCreate, FuelCollectionRead
from app.cache import invalidate_cache
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


def create_fuel_collection(
    collection: FuelCollectionCreate,
    session: Session
) -> FuelCollectionRead:
    """
    Cria uma nova coleta de combustível no banco de dados.
    
    Args:
        collection: Dados da coleta a ser criada
        session: Sessão do banco de dados
    
    Returns:
        FuelCollectionRead com os dados da coleta criada
    
    Raises:
        HTTPException: Se houver erro ao salvar no banco
    """
    # Cria o objeto SQLModel a partir do Pydantic Model recebido
    db_collection = FuelCollection.model_validate(collection)
    
    try:
        session.add(db_collection)
        session.commit()
        session.refresh(db_collection)
        
        # Invalida cache dos KPIs quando novos dados são inseridos
        invalidate_cache("kpi:*")
        
        return FuelCollectionRead.model_validate(db_collection)
        
    except Exception as e:
        logger.error(f"Erro ao salvar dados: {e}")
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar a ingestão dos dados."
        )
