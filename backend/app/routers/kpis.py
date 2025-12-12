from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.dependencies import get_session
from app.schemas import AvgPriceByFuel, VolumeByVehicle
from app.services.kpi_service import get_avg_price_by_fuel as get_avg_price_service
from app.services.kpi_service import get_volume_by_vehicle as get_volume_service

router = APIRouter(prefix="/kpis", tags=["KPIs"])


@router.get("/avg-price-by-fuel", response_model=list[AvgPriceByFuel])
def get_avg_price_by_fuel(session: Session = Depends(get_session)):
    """
    Retorna a média de preço por tipo de combustível.
    
    Utiliza agregação SQL (AVG, GROUP BY) para calcular o preço médio
    de cada tipo de combustível baseado em todos os registros.
    """
    return get_avg_price_service(session)


@router.get("/volume-by-vehicle", response_model=list[VolumeByVehicle])
def get_volume_by_vehicle(session: Session = Depends(get_session)):
    """
    Retorna o volume total consumido agrupado por tipo de veículo.
    
    Utiliza agregação SQL (SUM, GROUP BY) para calcular quanto cada
    tipo de veículo consumiu ao longo do tempo.
    
    Útil para responder: \"Quanto as carretas consumiram vs. carros?\"
    """
    return get_volume_service(session)
