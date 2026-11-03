from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


#url para o banco de dados SQLite local
SQLALCHEMY_DATABASE_URL = "sqlite:///./livraria.db"


#criacao da engine de conexão do SQLAlchemy
# para permitir múltiplos threads em requisições web, 'check_same_thread=False' é necessário no SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criação da fábrica de sessões do SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#classe base para os modelos ORM do SQLAlchemy
Base = declarative_base()


#(Injeção de Dependências com Depends)
# Abre uma nova sessão do banco a cada requisição e garante que será fechada no final
def get_db():
    db = SessionLocal()
    try:
        yield db  # Disponibiliza a sessão para o endpoint
    finally:
        db.close()  # Fecha a sessão liberando a conexão
