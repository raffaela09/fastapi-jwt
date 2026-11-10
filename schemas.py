from pydantic import BaseModel, ConfigDict, EmailStr


#schema base com os campos comuns de um livro
class BookBase(BaseModel):
    name: str
    description: str | None = None
    price: float


#schema utilizado para criação de livro (o ID é opcional pois pode ser gerado pelo banco)
class BookCreate(BookBase):
    id: int | None = None


#schema utilizado para atualização de livro
class BookUpdate(BookBase):
    pass


#schema completo de resposta retornado pela API
class Book(BookBase):
    id: int

    # Permite ao Pydantic ler os dados diretamente de objetos do SQLAlchemy (ORM mode)
    model_config = ConfigDict(from_attributes=True)


# Schema para cadastro de novo usuário
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Schema para login via JSON
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema de retorno dos dados do usuário (sem expor a senha)
class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


# Schema para retorno do Token JWT
class Token(BaseModel):
    access_token: str
    token_type: str


# Schema para os dados contidos no Token JWT
class TokenData(BaseModel):
    email: str | None = None
