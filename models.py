from sqlalchemy import Column, Float, Integer, String
from database import Base

#mmodelo ORM do SQLAlchemy que representa a tabela 'books' no banco de dados
class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)  
    name = Column(String, index=True, nullable=False)   
    description = Column(String, nullable=True)        
    price = Column(Float, nullable=False)              


#modelo ORM do SQLAlchemy que representa a tabela 'users' no banco de dados
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
