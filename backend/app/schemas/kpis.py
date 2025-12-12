from sqlmodel import SQLModel, Field
from app.schemas.responses import FuelCollectionRead


class AvgPriceByFuel(SQLModel):
    """Média de preço por tipo de combustível"""
    fuel_type: str
    avg_price: float = Field(description="Preço médio em R$/litro")
    total_records: int = Field(description="Número de registros computados")


class VolumeByVehicle(SQLModel):
    """Volume total consumido por tipo de veículo"""
    vehicle_type: str
    total_volume: float = Field(description="Volume total em litros")
    total_records: int = Field(description="Número de abastecimentos")


class DriverReport(SQLModel):
    """Relatório individual de motorista"""
    driver_name: str
    driver_cpf_masked: str
    total_refuels: int = Field(description="Total de abastecimentos")
    total_spent: float = Field(description="Total gasto em R$")
    total_volume: float = Field(description="Volume total abastecido em litros")
    favorite_fuel: str = Field(description="Combustível mais utilizado")
    refuels: list[FuelCollectionRead] = Field(description="Histórico de abastecimentos")
