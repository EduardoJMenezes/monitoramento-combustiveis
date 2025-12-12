from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.dependencies import get_session
from app.schemas import DriverReport
from app.services.report_service import get_driver_report as get_driver_report_service

router = APIRouter(prefix="/reports", tags=["Relatórios"])


@router.get("/drivers", response_model=DriverReport)
def get_driver_report(
    search: str = Query(..., description="CPF (11 dígitos) ou Nome do motorista"),
    session: Session = Depends(get_session)
):
    """
    Retorna relatório completo de um motorista específico.
    
    Busca por CPF (exato) ou Nome (parcial) e retorna:
    - Total de abastecimentos
    - Total gasto (R$)
    - Volume total abastecido
    - Combustível favorito
    - Histórico completo de abastecimentos
    """
    return get_driver_report_service(search, session)
