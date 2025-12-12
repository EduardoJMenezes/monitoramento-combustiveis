from sqlmodel import Session, select, func
from app.models import FuelCollection
from app.schemas import AvgPriceByFuel, VolumeByVehicle
from app.cache import cached


@cached("kpi:avg_price", ttl=600, skip_args=1)  # Cache de 10 minutos, ignora session
def get_avg_price_by_fuel(session: Session) -> list[AvgPriceByFuel]:
    """
    Calcula a média de preço por tipo de combustível.
    
    Utiliza agregação SQL (AVG, GROUP BY) para calcular o preço médio
    de cada tipo de combustível baseado em todos os registros.
    
    Args:
        session: Sessão do banco de dados
    
    Returns:
        Lista de AvgPriceByFuel com fuel_type, avg_price e total_records
    """
    # Query SQL com agregação
    avg_price_col = func.avg(FuelCollection.sale_price).label("avg_price")
    statement = select(
        FuelCollection.fuel_type,
        avg_price_col,
        func.count(FuelCollection.id).label("total_records")
    ).group_by(FuelCollection.fuel_type).order_by(avg_price_col.desc())
    
    results = session.exec(statement).all()
    
    # Formatar resposta
    return [
        AvgPriceByFuel(
            fuel_type=row[0],
            avg_price=round(row[1], 2),
            total_records=row[2]
        )
        for row in results
    ]


@cached("kpi:volume", ttl=600, skip_args=1)  # Cache de 10 minutos, ignora session
def get_volume_by_vehicle(session: Session) -> list[VolumeByVehicle]:
    """
    Calcula o volume total consumido por tipo de veículo.
    
    Utiliza agregação SQL (SUM, GROUP BY) para calcular quanto cada
    tipo de veículo consumiu ao longo do tempo.
    
    Args:
        session: Sessão do banco de dados
    
    Returns:
        Lista de VolumeByVehicle com vehicle_type, total_volume e total_records
    """
    # Query SQL com agregação
    total_volume_col = func.sum(FuelCollection.volume_sold).label("total_volume")
    statement = select(
        FuelCollection.vehicle_type,
        total_volume_col,
        func.count(FuelCollection.id).label("total_records")
    ).group_by(FuelCollection.vehicle_type).order_by(total_volume_col.desc())
    
    results = session.exec(statement).all()
    
    # Formatar resposta
    return [
        VolumeByVehicle(
            vehicle_type=row[0],
            total_volume=round(row[1], 2),
            total_records=row[2]
        )
        for row in results
    ]
