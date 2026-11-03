from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    name: str
    description: str | None = None
    price: float


class BookCreate(BookBase):
    id: int | None = None


class BookUpdate(BookBase):
    pass


class Book(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
