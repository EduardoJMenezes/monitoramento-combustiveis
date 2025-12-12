import pytest
from app.services.ingest_service import create_fuel_collection
from app.schemas import FuelCollectionCreate
from app.models import FuelCollection
from fastapi import HTTPException


def test_create_fuel_collection_success(session, sample_collection_data):
    """Testa criação bem-sucedida de uma coleta"""
    # Arrange
    collection_data = FuelCollectionCreate(**sample_collection_data)
    
    # Act
    result = create_fuel_collection(collection_data, session)
    
    # Assert
    assert result.id is not None
    assert result.driver_name == "João Silva"
    assert result.fuel_type == "Gasolina"
    assert result.driver_cpf_masked == "123.***.***.01"
    
    # Verificar que foi salvo no banco
    db_collection = session.get(FuelCollection, result.id)
    assert db_collection is not None
    assert db_collection.driver_cpf == "12345678901"


def test_create_fuel_collection_invalid_cpf(session):
    """Testa validação de CPF inválido"""
    # Arrange
    invalid_data = {
        "store_id": "12345678000190",
        "store_name": "Posto Teste",
        "city": "São Paulo",
        "state": "SP",
        "fuel_type": "Gasolina",
        "sale_price": 5.89,
        "volume_sold": 45.5,
        "driver_name": "João Silva",
        "driver_cpf": "123",  # CPF inválido (menos de 11 dígitos)
        "vehicle_plate": "ABC1234",
        "vehicle_type": "Carro"
    }
    
    # Act & Assert
    with pytest.raises(Exception):  # Pydantic ValidationError
        FuelCollectionCreate(**invalid_data)


def test_create_fuel_collection_invalid_fuel_type(session):
    """Testa validação de tipo de combustível inválido"""
    # Arrange
    invalid_data = {
        "store_id": "12345678000190",
        "store_name": "Posto Teste",
        "city": "São Paulo",
        "state": "SP",
        "fuel_type": "GNV",  # Tipo não permitido
        "sale_price": 5.89,
        "volume_sold": 45.5,
        "driver_name": "João Silva",
        "driver_cpf": "12345678901",
        "vehicle_plate": "ABC1234",
        "vehicle_type": "Carro"
    }
    
    # Act & Assert
    with pytest.raises(Exception):  # Pydantic ValidationError
        FuelCollectionCreate(**invalid_data)


def test_create_fuel_collection_negative_price(session):
    """Testa validação de preço negativo"""
    # Arrange
    invalid_data = {
        "store_id": "12345678000190",
        "store_name": "Posto Teste",
        "city": "São Paulo",
        "state": "SP",
        "fuel_type": "Gasolina",
        "sale_price": -5.89,  # Preço negativo
        "volume_sold": 45.5,
        "driver_name": "João Silva",
        "driver_cpf": "12345678901",
        "vehicle_plate": "ABC1234",
        "vehicle_type": "Carro"
    }
    
    # Act & Assert
    with pytest.raises(Exception):  # Pydantic ValidationError
        FuelCollectionCreate(**invalid_data)
