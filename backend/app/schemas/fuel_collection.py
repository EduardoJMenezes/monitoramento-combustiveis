from sqlmodel import SQLModel, Field
from pydantic import field_validator, computed_field
import re

# Definição dos tipos de combustível e veículo para melhor tipagem e validação
FUEL_TYPES = ["Gasolina", "Etanol", "Diesel S10"]
VEHICLE_TYPES = ["Carro", "Moto", "Caminhão Leve", "Carreta", "Ônibus"]


class FuelCollectionCreate(SQLModel):
    """Schema para criação de nova coleta"""
    store_id: str
    store_name: str
    city: str
    state: str
    fuel_type: str
    sale_price: float = Field(ge=0, description="Preço em Reais por litro")
    volume_sold: float = Field(ge=0, description="Volume em litros")
    driver_name: str
    driver_cpf: str = Field(min_length=11, max_length=11, description="CPF com 11 dígitos")
    vehicle_plate: str
    vehicle_type: str
    
    @field_validator('driver_cpf')
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        """Valida se o CPF contém apenas números"""
        if not re.match(r'^\d{11}$', v):
            raise ValueError('CPF deve conter exatamente 11 dígitos numéricos')
        return v
    
    @field_validator('fuel_type')
    @classmethod
    def validate_fuel_type(cls, v: str) -> str:
        """Valida se o tipo de combustível é válido"""
        if v not in FUEL_TYPES:
            raise ValueError(f'Tipo de combustível deve ser um de: {FUEL_TYPES}')
        return v
    
    @field_validator('vehicle_type')
    @classmethod
    def validate_vehicle_type(cls, v: str) -> str:
        """Valida se o tipo de veículo é válido"""
        if v not in VEHICLE_TYPES:
            raise ValueError(f'Tipo de veículo deve ser um de: {VEHICLE_TYPES}')
        return v
