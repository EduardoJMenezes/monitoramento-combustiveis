from sqlmodel import create_engine, SQLModel, Session
import os
import logging

logger = logging.getLogger(__name__)

# URL de conexão lida da variável de ambiente
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    logger.error("A variável de ambiente DATABASE_URL não foi definida!")
    raise ValueError("DATABASE_URL must be set.")

# Cria o objeto Engine para conexão
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Cria as tabelas no DB se elas não existirem."""
    logger.info("Tentando criar tabelas no DB...")
    SQLModel.metadata.create_all(engine)
    logger.info("Tabelas criadas ou já existentes.")
