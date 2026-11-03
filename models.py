from sqlalchemy import Column, Float, Integer, String
from database import Base

# Modelo ORM do SQLAlchemy que representa a tabela 'books' no banco de dados
class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True, nullable=False)   
    description = Column(String, nullable=True)        
    price = Column(Float, nullable=False)              
