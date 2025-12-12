from typing import Generator
from sqlmodel import Session
from app.database import engine


def get_session() -> Generator[Session, None, None]:
    """
    Dependência do FastAPI para injetar sessão de banco de dados.
    
    Yields:
        Session: Sessão do SQLModel para operações de banco de dados
    
    Example:
        @app.get("/items")
        def read_items(session: Session = Depends(get_session)):
            items = session.exec(select(Item)).all()
            return items
    """
    with Session(engine) as session:
        yield session
