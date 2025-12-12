import pytest
from app.services.kpi_service import get_avg_price_by_fuel, get_volume_by_vehicle


def test_get_avg_price_by_fuel_empty_database(session):
    """Testa cálculo de preço médio em banco vazio"""
    # Act
    result = get_avg_price_by_fuel(session)
    
    # Assert
    assert len(result) == 0


def test_get_avg_price_by_fuel_with_data(session, create_sample_collections):
    """Testa cálculo de preço médio com dados"""
    # Act
    result = get_avg_price_by_fuel(session)
    
    # Assert
    assert len(result) == 3  # 3 tipos de combustível
    
    # Verificar estrutura dos dados
    for item in result:
        assert hasattr(item, 'fuel_type')
        assert hasattr(item, 'avg_price')
        assert hasattr(item, 'total_records')
        assert item.avg_price > 0
        assert item.total_records > 0
    
    # Verificar que Diesel S10 tem o preço mais alto (ordenado desc)
    assert result[0].fuel_type == "Diesel S10"
    assert result[0].avg_price == 6.50
    assert result[0].total_records == 1


def test_get_avg_price_by_fuel_calculation(session, create_sample_collections):
    """Testa se o cálculo da média está correto"""
    # Adicionar mais uma gasolina para testar média
    from app.models import FuelCollection
    
    extra_collection = FuelCollection(
        store_id="99999999000199",
        store_name="Posto D",
        city="Brasília",
        state="DF",
        fuel_type="Gasolina",
        sale_price=5.50,  # Média com 6.00 = 5.75
        volume_sold=30.0,
        driver_name="Ana Costa",
        driver_cpf="55566677788",
        vehicle_plate="GHI3456",
        vehicle_type="Carro"
    )
    session.add(extra_collection)
    session.commit()
    
    # Act
    result = get_avg_price_by_fuel(session)
    
    # Assert
    gasolina = [r for r in result if r.fuel_type == "Gasolina"][0]
    assert gasolina.avg_price == 5.75  # (6.00 + 5.50) / 2
    assert gasolina.total_records == 2


def test_get_volume_by_vehicle_empty_database(session):
    """Testa cálculo de volume em banco vazio"""
    # Act
    result = get_volume_by_vehicle(session)
    
    # Assert
    assert len(result) == 0


def test_get_volume_by_vehicle_with_data(session, create_sample_collections):
    """Testa cálculo de volume por veículo com dados"""
    # Act
    result = get_volume_by_vehicle(session)
    
    # Assert
    assert len(result) == 3  # 3 tipos de veículo
    
    # Verificar estrutura dos dados
    for item in result:
        assert hasattr(item, 'vehicle_type')
        assert hasattr(item, 'total_volume')
        assert hasattr(item, 'total_records')
        assert item.total_volume > 0
        assert item.total_records > 0
    
    # Verificar que Carreta tem o maior volume (ordenado desc)
    assert result[0].vehicle_type == "Carreta"
    assert result[0].total_volume == 150.0
    assert result[0].total_records == 1


def test_get_volume_by_vehicle_calculation(session, create_sample_collections):
    """Testa se o cálculo do volume total está correto"""
    # Adicionar mais um carro para testar soma
    from app.models import FuelCollection
    
    extra_collection = FuelCollection(
        store_id="88888888000188",
        store_name="Posto E",
        city="Curitiba",
        state="PR",
        fuel_type="Etanol",
        sale_price=4.20,
        volume_sold=35.0,  # Total carros: 50.0 + 35.0 = 85.0
        driver_name="Pedro Lima",
        driver_cpf="44455566677",
        vehicle_plate="JKL7890",
        vehicle_type="Carro"
    )
    session.add(extra_collection)
    session.commit()
    
    # Act
    result = get_volume_by_vehicle(session)
    
    # Assert
    carro = [r for r in result if r.vehicle_type == "Carro"][0]
    assert carro.total_volume == 85.0  # 50.0 + 35.0
    assert carro.total_records == 2


def test_get_volume_by_vehicle_ordering(session, create_sample_collections):
    """Testa se os resultados estão ordenados por volume (desc)"""
    # Act
    result = get_volume_by_vehicle(session)
    
    # Assert
    volumes = [item.total_volume for item in result]
    assert volumes == sorted(volumes, reverse=True)  # Deve estar em ordem decrescente
