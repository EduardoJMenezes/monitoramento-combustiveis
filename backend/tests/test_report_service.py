import pytest
from app.services.report_service import get_driver_report
from app.models import FuelCollection
from fastapi import HTTPException


def test_get_driver_report_by_cpf(session, create_sample_collections):
    """Testa busca de relatório por CPF"""
    # Act
    result = get_driver_report("12345678901", session)
    
    # Assert
    assert result.driver_name == "João Silva"
    assert result.driver_cpf_masked == "123.***.***.01"
    assert result.total_refuels == 1
    assert result.total_spent == 300.0  # 6.00 * 50.0
    assert result.total_volume == 50.0
    assert result.favorite_fuel == "Gasolina"
    assert len(result.refuels) == 1


def test_get_driver_report_by_name(session, create_sample_collections):
    """Testa busca de relatório por nome (parcial)"""
    # Act
    result = get_driver_report("Maria", session)
    
    # Assert
    assert result.driver_name == "Maria Santos"
    assert result.driver_cpf_masked == "987.***.***.09"
    assert result.total_refuels == 1
    assert result.total_spent == 180.0  # 4.50 * 40.0
    assert result.total_volume == 40.0
    assert result.favorite_fuel == "Etanol"


def test_get_driver_report_name_case_insensitive(session, create_sample_collections):
    """Testa busca por nome case insensitive"""
    # Act
    result = get_driver_report("carlos", session)
    
    # Assert
    assert result.driver_name == "Carlos Oliveira"
    assert result.total_refuels == 1


def test_get_driver_report_not_found_cpf(session):
    """Testa erro quando CPF não existe"""
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_driver_report("99999999999", session)
    
    assert exc_info.value.status_code == 404
    assert "Nenhum registro encontrado" in exc_info.value.detail


def test_get_driver_report_not_found_name(session):
    """Testa erro quando nome não existe"""
    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_driver_report("Inexistente", session)
    
    assert exc_info.value.status_code == 404


def test_get_driver_report_multiple_refuels(session):
    """Testa relatório com múltiplos abastecimentos do mesmo motorista"""
    # Arrange - Criar múltiplos abastecimentos
    collections = [
        FuelCollection(
            store_id="12345678000190",
            store_name="Posto A",
            city="São Paulo",
            state="SP",
            fuel_type="Gasolina",
            sale_price=6.00,
            volume_sold=50.0,
            driver_name="João Silva",
            driver_cpf="12345678901",
            vehicle_plate="ABC1234",
            vehicle_type="Carro"
        ),
        FuelCollection(
            store_id="98765432000111",
            store_name="Posto B",
            city="Rio de Janeiro",
            state="RJ",
            fuel_type="Etanol",
            sale_price=4.50,
            volume_sold=40.0,
            driver_name="João Silva",
            driver_cpf="12345678901",
            vehicle_plate="ABC1234",
            vehicle_type="Carro"
        ),
        FuelCollection(
            store_id="11122233000144",
            store_name="Posto C",
            city="São Paulo",
            state="SP",
            fuel_type="Gasolina",
            sale_price=6.20,
            volume_sold=45.0,
            driver_name="João Silva",
            driver_cpf="12345678901",
            vehicle_plate="ABC1234",
            vehicle_type="Carro"
        ),
    ]
    
    for collection in collections:
        session.add(collection)
    session.commit()
    
    # Act
    result = get_driver_report("12345678901", session)
    
    # Assert
    assert result.total_refuels == 3
    assert result.total_spent == 759.0  # (6.00*50) + (4.50*40) + (6.20*45)
    assert result.total_volume == 135.0  # 50 + 40 + 45
    assert result.favorite_fuel == "Gasolina"  # 2 gasolina vs 1 etanol
    assert len(result.refuels) == 3


def test_get_driver_report_favorite_fuel_calculation(session):
    """Testa cálculo do combustível favorito"""
    # Arrange - 2 Etanol, 1 Gasolina
    collections = [
        FuelCollection(
            store_id="12345678000190",
            store_name="Posto A",
            city="São Paulo",
            state="SP",
            fuel_type="Etanol",
            sale_price=4.50,
            volume_sold=40.0,
            driver_name="Ana Costa",
            driver_cpf="11111111111",
            vehicle_plate="XYZ1234",
            vehicle_type="Carro"
        ),
        FuelCollection(
            store_id="98765432000111",
            store_name="Posto B",
            city="Rio de Janeiro",
            state="RJ",
            fuel_type="Etanol",
            sale_price=4.60,
            volume_sold=35.0,
            driver_name="Ana Costa",
            driver_cpf="11111111111",
            vehicle_plate="XYZ1234",
            vehicle_type="Carro"
        ),
        FuelCollection(
            store_id="11122233000144",
            store_name="Posto C",
            city="São Paulo",
            state="SP",
            fuel_type="Gasolina",
            sale_price=6.00,
            volume_sold=50.0,
            driver_name="Ana Costa",
            driver_cpf="11111111111",
            vehicle_plate="XYZ1234",
            vehicle_type="Carro"
        ),
    ]
    
    for collection in collections:
        session.add(collection)
    session.commit()
    
    # Act
    result = get_driver_report("11111111111", session)
    
    # Assert
    assert result.favorite_fuel == "Etanol"  # Mais frequente
    assert result.total_refuels == 3
