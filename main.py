from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

app = FastAPI()


@app.get("/")
async def root():
    return {"Mensagem": "Sistema de Livraria Online"}


@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    if book.id is not None:
        existing_book = db.query(models.BookModel).filter(models.BookModel.id == book.id).first()
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Livro com este ID já existe.",
            )

    db_book = models.BookModel(
        id=book.id,
        name=book.name,
        description=book.description,
        price=book.price,
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


# retorna todos os livros cadastrados
@app.get("/books/", response_model=list[schemas.Book])
async def get_all_books(db: Session = Depends(get_db)):
    return db.query(models.BookModel).all()


@app.get("/books/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    return book


# deleta o livro pelo id, caso nao exista retorna 404
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    db.delete(book)
    db.commit()
    return


# atualizacao do livro pelo id, caso nao exista retorna 404
@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, updated_book: schemas.BookUpdate, db: Session = Depends(get_db)):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")

    book.name = updated_book.name
    book.description = updated_book.description
    book.price = updated_book.price

    db.commit()
    db.refresh(book)
    return book
