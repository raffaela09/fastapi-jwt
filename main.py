from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

import models
import schemas
from database import get_db

app = FastAPI()


@app.get("/")
async def root():
    return {"Mensagem": "Sistema de Livraria Online"}


# Rota para cadastrar um novo livro
# Recebe os dados validados pelo schema BookCreate e retorna o schema Book com status 201 Created
@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: schemas.BookCreate,  # Dados do livro enviados no corpo da requisição (validados pelo Pydantic)
    db: Session = Depends(get_db),  # Injeção de dependência: abre e gerencia a sessão do banco
):
    # Se o ID foi informado na requisição, verifica se já existe outro livro com esse mesmo ID no banco
    if book.id is not None:
        existing_book = db.query(models.BookModel).filter(models.BookModel.id == book.id).first()
        if existing_book:
            # Caso o ID já exista, interrompe a requisição com código 400 Bad Request
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Livro com este ID já existe.",
            )

    # Converte os dados do schema Pydantic para uma instância do Model do SQLAlchemy
    db_book = models.BookModel(
        id=book.id,
        name=book.name,
        description=book.description,
        price=book.price,
    )

    # 1. Adiciona o novo livro na sessão do banco de dados (fila de operações)
    db.add(db_book)

    # 2. Executa a transação no banco (efetiva o INSERT no SQLite)
    db.commit()

    # 3. Atualiza o objeto com os dados gerados pelo banco (ex: ID auto-incremental)
    db.refresh(db_book)

    # Retorna o livro cadastrado (o FastAPI serializa automaticamente para o response_model)
    return db_book


# Rota para listar todos os livros cadastrados no banco de dados
@app.get("/books/", response_model=list[schemas.Book])
async def get_all_books(db: Session = Depends(get_db)):
    # Faz uma consulta SELECT * FROM books e retorna todos os registros
    return db.query(models.BookModel).all()


# Rota para buscar um livro específico pelo seu ID
@app.get("/books/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    # Faz um SELECT WHERE id = book_id buscando o primeiro resultado
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        # Se não encontrar o livro, retorna erro 404 Not Found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    return book


# Rota para deletar um livro pelo ID (retorna status 204 No Content se der certo)
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    # Busca o livro no banco antes de deletar
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        # Se o livro não existir, retorna 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    
    # Remove o registro da sessão e confirma a remoção no banco com commit
    db.delete(book)
    db.commit()
    return


# Rota para atualizar os dados de um livro existente pelo ID
@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(
    book_id: int, 
    updated_book: schemas.BookUpdate, 
    db: Session = Depends(get_db)
):
    # Localiza o livro pelo ID no banco
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        # Se não encontrar, retorna 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")

    # Atualiza os atributos do objeto com os novos valores recebidos
    book.name = updated_book.name
    book.description = updated_book.description
    book.price = updated_book.price

    # Salva as alterações no banco e atualiza o objeto
    db.commit()
    db.refresh(book)
    return book
