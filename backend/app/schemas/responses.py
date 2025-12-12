from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import computed_field
from app.models import FuelCollectionBase


class FuelCollectionRead(FuelCollectionBase):
    """Schema para leitura de coleta"""
    id: int
    collection_date: datetime
    
    @computed_field
    @property
    def driver_cpf_masked(self) -> str:
        """Retorna o CPF mascarado (XXX.***.***.XX)"""
        cpf = self.driver_cpf
        if len(cpf) == 11:
            return f"{cpf[:3]}.***.***.{cpf[-2:]}"
        return "***.***.***-**"


class PaginatedResponse(SQLModel):
    """Schema genérico para respostas paginadas"""
    total: int = Field(description="Total de registros no banco")
    page: int = Field(description="Página atual")
    page_size: int = Field(description="Tamanho da página")
    data: list[FuelCollectionRead] = Field(description="Lista de coletas")
