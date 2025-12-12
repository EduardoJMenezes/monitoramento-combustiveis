from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.dependencies import get_session
from app.schemas import FuelCollectionCreate, FuelCollectionRead
from app.services.ingest_service import create_fuel_collection

router = APIRouter(prefix="", tags=["Ingestão"])


@router.post("/ingest", response_model=FuelCollectionRead, status_code=status.HTTP_201_CREATED)
def ingest_data(collection: FuelCollectionCreate, session: Session = Depends(get_session)):
    """
    Recebe e salva os dados brutos de abastecimento no banco de dados.
    
    Args:
        collection: Dados da coleta a ser criada
        session: Sessão do banco de dados (injetada)
    
    Returns:
        FuelCollectionRead com os dados da coleta criada
    """
    return create_fuel_collection(collection, session)
