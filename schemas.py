from pydantic import BaseModel, ConfigDict


# Schema base com os campos comuns de um livro
class BookBase(BaseModel):
    name: str
    description: str | None = None
    price: float


# Schema utilizado para criação de livro (o ID é opcional pois pode ser gerado pelo banco)
class BookCreate(BookBase):
    id: int | None = None


# Schema utilizado para atualização de livro
class BookUpdate(BookBase):
    pass


# Schema completo de resposta retornado pela API
class Book(BookBase):
    id: int

    # Permite ao Pydantic ler os dados diretamente de objetos do SQLAlchemy (ORM mode)
    model_config = ConfigDict(from_attributes=True)
