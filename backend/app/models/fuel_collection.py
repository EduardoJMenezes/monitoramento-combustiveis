from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class FuelCollectionBase(SQLModel):
    """Modelo base com campos comuns"""
    store_id: str = Field(index=True, max_length=50)
    store_name: str
    city: str
    state: str
    collection_date: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    fuel_type: str = Field(index=True, description="Gasolina, Etanol, Diesel S10")
    sale_price: float = Field(ge=0)
    volume_sold: float = Field(ge=0)
    driver_name: str
    driver_cpf: str = Field(max_length=11)
    vehicle_plate: str = Field(max_length=10)
    vehicle_type: str = Field(index=True, description="Carro, Carreta, etc.")


class FuelCollection(FuelCollectionBase, table=True):
    """Tabela principal de coletas de combustível no PostgreSQL"""
    __tablename__ = "fuelcollection"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    
    class Config:
        from_attributes = True
