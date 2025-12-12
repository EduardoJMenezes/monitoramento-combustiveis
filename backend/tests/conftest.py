import pytest
from sqlmodel import create_engine, SQLModel, Session
from sqlalchemy.pool import StaticPool
from app.models import FuelCollection


@pytest.fixture(name="session")
def session_fixture():
    """
    Cria uma sessão de banco de dados em memória para testes.
    Cada teste recebe um banco limpo e isolado.
    """
    # Criar engine SQLite em memória
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Criar todas as tabelas
    SQLModel.metadata.create_all(engine)
    
    # Criar sessão
    with Session(engine) as session:
        yield session
    
    # Cleanup não é necessário pois o banco está em memória


@pytest.fixture
def sample_collection_data():
    """Dados de exemplo para testes"""
    return {
        "store_id": "12345678000190",
        "store_name": "Posto Teste",
        "city": "São Paulo",
        "state": "SP",
        "fuel_type": "Gasolina",
        "sale_price": 5.89,
        "volume_sold": 45.5,
        "driver_name": "João Silva",
        "driver_cpf": "12345678901",
        "vehicle_plate": "ABC1234",
        "vehicle_type": "Carro"
    }


@pytest.fixture
def create_sample_collections(session):
    """
    Cria múltiplas coletas de exemplo no banco de testes.
    Útil para testar queries com múltiplos registros.
    """
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
            driver_name="Maria Santos",
            driver_cpf="98765432109",
            vehicle_plate="XYZ5678",
            vehicle_type="Moto"
        ),
        FuelCollection(
            store_id="11122233000144",
            store_name="Posto C",
            city="São Paulo",
            state="SP",
            fuel_type="Diesel S10",
            sale_price=6.50,
            volume_sold=150.0,
            driver_name="Carlos Oliveira",
            driver_cpf="11122233344",
            vehicle_plate="DEF9012",
            vehicle_type="Carreta"
        ),
    ]
    
    for collection in collections:
        session.add(collection)
    session.commit()
    
    return collections
