from sqlmodel import Session, select
from app.models import FuelCollection
from app.schemas import FuelCollectionRead, DriverReport
from fastapi import HTTPException, status


def get_driver_report(
    search: str,
    session: Session
) -> DriverReport:
    """
    Gera relatório completo de um motorista específico.
    
    Busca por CPF (exato) ou Nome (parcial) e retorna estatísticas
    completas incluindo total de abastecimentos, gastos e combustível favorito.
    
    Args:
        search: CPF (11 dígitos) ou Nome do motorista
        session: Sessão do banco de dados
    
    Returns:
        DriverReport com estatísticas e histórico completo
    
    Raises:
        HTTPException: Se nenhum registro for encontrado
    """
    # Determinar se é CPF ou Nome
    is_cpf = search.isdigit() and len(search) == 11
    
    # Construir query base
    if is_cpf:
        statement = select(FuelCollection).where(FuelCollection.driver_cpf == search)
    else:
        statement = select(FuelCollection).where(FuelCollection.driver_name.ilike(f"%{search}%"))
    
    # Executar query
    results = session.exec(statement.order_by(FuelCollection.collection_date.desc())).all()
    
    if not results:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Nenhum registro encontrado para: {search}"
        )
    
    # Calcular estatísticas
    total_refuels = len(results)
    total_spent = sum(r.sale_price * r.volume_sold for r in results)
    total_volume = sum(r.volume_sold for r in results)
    
    # Calcular combustível favorito (mais utilizado)
    fuel_counts = {}
    for r in results:
        fuel_counts[r.fuel_type] = fuel_counts.get(r.fuel_type, 0) + 1
    favorite_fuel = max(fuel_counts, key=fuel_counts.get)
    
    # Pegar dados do primeiro registro para nome e CPF
    first_record = results[0]
    
    # Converter para FuelCollectionRead
    refuels = [FuelCollectionRead.model_validate(r) for r in results]
    
    return DriverReport(
        driver_name=first_record.driver_name,
        driver_cpf_masked=f"{first_record.driver_cpf[:3]}.***.***.{first_record.driver_cpf[-2:]}",
        total_refuels=total_refuels,
        total_spent=round(total_spent, 2),
        total_volume=round(total_volume, 2),
        favorite_fuel=favorite_fuel,
        refuels=refuels
    )
