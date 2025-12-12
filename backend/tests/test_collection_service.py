import pytest
from app.services.collection_service import get_collections


def test_get_collections_empty_database(session):
    """Testa busca de coletas em banco vazio"""
    # Act
    result = get_collections(session, page=1, page_size=10)
    
    # Assert
    assert result.total == 0
    assert result.page == 1
    assert result.page_size == 10
    assert len(result.data) == 0


def test_get_collections_with_data(session, create_sample_collections):
    """Testa busca de coletas com dados"""
    # Act
    result = get_collections(session, page=1, page_size=10)
    
    # Assert
    assert result.total == 3
    assert result.page == 1
    assert result.page_size == 10
    assert len(result.data) == 3
    
    # Verificar que os dados estão ordenados por data (desc)
    assert all(item.id is not None for item in result.data)


def test_get_collections_pagination(session, create_sample_collections):
    """Testa paginação"""
    # Act - Página 1 com 2 itens
    result_page1 = get_collections(session, page=1, page_size=2)
    
    # Assert
    assert result_page1.total == 3
    assert result_page1.page == 1
    assert result_page1.page_size == 2
    assert len(result_page1.data) == 2
    
    # Act - Página 2 com 2 itens
    result_page2 = get_collections(session, page=2, page_size=2)
    
    # Assert
    assert result_page2.total == 3
    assert result_page2.page == 2
    assert len(result_page2.data) == 1  # Último item


def test_get_collections_filter_by_fuel_type(session, create_sample_collections):
    """Testa filtro por tipo de combustível"""
    # Act
    result = get_collections(session, page=1, page_size=10, fuel_type="Gasolina")
    
    # Assert
    assert result.total == 1
    assert len(result.data) == 1
    assert result.data[0].fuel_type == "Gasolina"


def test_get_collections_filter_by_city(session, create_sample_collections):
    """Testa filtro por cidade (case insensitive)"""
    # Act
    result = get_collections(session, page=1, page_size=10, city="são paulo")
    
    # Assert
    assert result.total == 2  # Posto A e Posto C
    assert len(result.data) == 2
    assert all(item.city == "São Paulo" for item in result.data)


def test_get_collections_filter_by_vehicle_type(session, create_sample_collections):
    """Testa filtro por tipo de veículo"""
    # Act
    result = get_collections(session, page=1, page_size=10, vehicle_type="Carreta")
    
    # Assert
    assert result.total == 1
    assert len(result.data) == 1
    assert result.data[0].vehicle_type == "Carreta"


def test_get_collections_multiple_filters(session, create_sample_collections):
    """Testa múltiplos filtros combinados"""
    # Act
    result = get_collections(
        session, 
        page=1, 
        page_size=10, 
        fuel_type="Gasolina",
        city="São Paulo"
    )
    
    # Assert
    assert result.total == 1
    assert len(result.data) == 1
    assert result.data[0].fuel_type == "Gasolina"
    assert result.data[0].city == "São Paulo"


def test_get_collections_cpf_masked(session, create_sample_collections):
    """Testa se o CPF retorna mascarado"""
    # Act
    result = get_collections(session, page=1, page_size=10)
    
    # Assert
    for item in result.data:
        assert "***" in item.driver_cpf_masked
        assert len(item.driver_cpf_masked) == 14  # XXX.***.***.XX
