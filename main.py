from datetime import timedelta
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import auth
import models
import schemas
from database import get_db

app = FastAPI(
    title="Sistema de Livraria Online com Autenticação OAuth2 e JWT",
    description="API com CRUD de livros e controle de acesso via tokens JWT.",
    version="2.0.0",
)


#rota pública de boas-vindas
@app.get("/")
async def root():
    return {"Mensagem": "Sistema de Livraria Online com Autenticação OAuth2 e JWT"}

#rota para cadastrar um novo usuário (Pública)
@app.post("/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    #verifica se já existe um usuário com o mesmo e-mail (responsabilidade HTTP / validação de regra)
    db_user = auth.get_user_by_email(db, email=user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um usuário cadastrado com este e-mail.",
        )

    #cria o usuário (hash da senha + persistência no banco) através de função especializada
    return auth.create_user(db=db, user=user_data)


#rota de login compatível com OAuth2 (utilizada pelo botão 'Authorize' do Swagger)
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


#rota alternativa de login via JSON (/login)
@app.post("/login", response_model=schemas.Token)
async def login_json(
    credentials: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires,
    )

    return {"access_token": access_token, "token_type": "bearer"}


#rota protegida para consultar os dados do usuário logado
@app.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(
    current_user: models.UserModel = Depends(auth.get_current_user),
):
    return current_user


#crud de livros (rotas protegidas e públicas)
#rtta protegida para cadastrar um novo livro (exige Bearer Token)
@app.post("/books/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(auth.get_current_user),  # Protegido por JWT
):
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


#rota publica para listar todos os livros
@app.get("/books/", response_model=list[schemas.Book])
async def get_all_books(db: Session = Depends(get_db)):
    return db.query(models.BookModel).all()


#rota publica para buscar um livro específico pelo ID
@app.get("/books/{book_id}", response_model=schemas.Book)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    return book


#rota protegida para deletar um livro pelo ID (exige Bearer Token)
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(auth.get_current_user),  # Protegido por JWT
):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    
    db.delete(book)
    db.commit()
    return


#rota protegida para atualizar um livro pelo ID (exige Bearer Token)
@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(
    book_id: int, 
    updated_book: schemas.BookUpdate, 
    db: Session = Depends(get_db),
    current_user: models.UserModel = Depends(auth.get_current_user),  # Protegido por JWT
):
    book = db.query(models.BookModel).filter(models.BookModel.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")

    book.name = updated_book.name
    book.description = updated_book.description
    book.price = updated_book.price

    db.commit()
    db.refresh(book)
    return book
