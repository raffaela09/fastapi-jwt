# Sistema de Livraria Online - FastAPI, SQLAlchemy & Autenticação OAuth2 com JWT

API REST desenvolvida com **FastAPI** para gerenciamento de livros, persistência de dados com **SQLite** e **SQLAlchemy**, controle de migrações com **Alembic**, e camada de segurança com **OAuth2 com Password Flow**, hash de senhas via **Passlib (bcrypt)** e tokens **JWT (PyJWT)**.

---

## 👥 Integrantes do Projeto

- Rafaela Virginio Franco 
- Izabella Araújo

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3.10+](https://www.python.org/)**
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e assíncrono.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM para comunicação com o banco de dados SQLite.
- **[Alembic](https://alembic.sqlalchemy.org/)**: Gerenciamento de migrações de esquema do banco de dados.
- **[Pydantic](https://docs.pydantic.dev/)**: Validação e serialização de dados estruturados.
- **[Passlib (bcrypt)](https://passlib.readthedocs.io/)**: Hashing seguro e verificação de senhas.
- **[PyJWT](https://pyjwt.readthedocs.io/)**: Geração e validação de tokens JWT.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI de alta performance.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/raffaela09/fastapi_persistencia_dados.git
cd projeto_rogerio
```

### 2. Criar e ativar o ambiente virtual

- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

- **Linux / macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Executar as migrações do banco de dados (Alembic)

Para criar ou atualizar as tabelas do banco de dados (`books` e `users`):

```bash
alembic upgrade head
```

### 5. Iniciar o servidor de desenvolvimento

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://127.0.0.1:8000`

---

## 📖 Documentação Interativa da API

Com a aplicação rodando, acesse a documentação interativa gerada pelo FastAPI:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 Rotas da API

### Autenticação & Usuários

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `POST` | `/users/` | **Público** | Cadastra um novo usuário (armazena senha com hash bcrypt) |
| `POST` | `/token` | **Público** | Endpoint OAuth2 Password: recebe credenciais e retorna o token JWT |
| `POST` | `/login` | **Público** | Endpoint alternativo de login recebendo JSON (`email` e `password`) |
| `GET` | `/users/me` | 🔒 **Protegido** | Retorna os dados do usuário atualmente autenticado |

### CRUD de Livros

| Método | Rota | Acesso | Descrição |
|---|---|---|---|
| `GET` | `/` | **Público** | Mensagem de status da API |
| `GET` | `/books/` | **Público** | Lista todos os livros cadastrados |
| `GET` | `/books/{book_id}` | **Público** | Obtém os detalhes de um livro específico |
| `POST` | `/books/` | 🔒 **Protegido** | Cadastra um novo livro (Requer Token JWT) |
| `PUT` | `/books/{book_id}` | 🔒 **Protegido** | Atualiza os dados de um livro existente (Requer Token JWT) |
| `DELETE` | `/books/{book_id}` | 🔒 **Protegido** | Remove um livro cadastrado (Requer Token JWT) |

---

## 🔑 Segurança e Autenticação (OAuth2 + JWT)

### Exemplo de Token JWT Gerado pelo Sistema

Abaixo está um exemplo real de token JWT gerado pela rota `/token` da aplicação:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3VhcmlvQGV4ZW1wbG8uY29tIiwiZXhwIjoxNzk0MzUwNjY1fQ.fJyv4WufeWNiAi6ABO3ypQl0PuPlB4rSva4pEzrpyCw
```

#### Estrutura do Token:

- **Header:**
  ```json
  {
    "alg": "HS256",
    "typ": "JWT"
  }
  ```
- **Payload:**
  ```json
  {
    "sub": "usuario@exemplo.com",
    "exp": 1794350665
  }
  ```
- **Signature:** Assinatura criptográfica HMAC SHA-256 baseada na chave secreta da aplicação.

---

## 🧪 Como Testar o Login e Rotas Protegidas pelo Swagger UI

1. Abra o navegador em [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
2. **Cadastre um usuário:**
   - Expanda a rota `POST /users/`.
   - Clique em **Try it out**.
   - No JSON, informe um e-mail válido e uma senha (ex: `{"email": "aluno@teste.com", "password": "senha123"}`).
   - Clique em **Execute** e confirme o retorno `201 Created`.
3. **Autentique-se pelo Swagger:**
   - No topo da página do Swagger, clique no botão verde **Authorize** (com ícone de cadeado).
   - No formulário que abrir:
     - No campo **username**, digite o e-mail cadastrado (ex: `aluno@teste.com`).
     - No campo **password**, digite a senha cadastrada (ex: `senha123`).
   - Clique em **Authorize** e depois em **Close**.
4. **Testar as Rotas:**
   - **Rotas de Leitura (Públicas):** Acesse `GET /books/` ou `GET /books/{id}`. Elas respondem com sucesso com ou sem autenticação.
   - **Rotas Sensíveis (Protegidas):**
     - Enquanto estiver autenticado, teste `POST /books/`, `PUT /books/{id}` ou `DELETE /books/{id}`. As requisições serão autorizadas com sucesso.
     - Para testar a proteção, clique novamente no botão **Authorize**, clique em **Logout**, e tente executar `POST /books/`. A API responderá com `401 Unauthorized` e mensagem `{"detail": "Not authenticated"}`.

---

## 📁 Estrutura de Arquivos

```text
├── alembic/                  # Diretório de migrações do Alembic
│   ├── versions/             # Histórico de migrações (books e users)
│   │   ├── 2f8310e299c2_create_books_table.py
│   │   └── 53a72841395e_create_users_table.py
│   └── env.py                # Configuração do ambiente Alembic
├── alembic.ini               # Configurações do Alembic
├── auth.py                   # Lógica de segurança, hash de senha e validação JWT
├── database.py               # Configuração do SQLAlchemy e sessão do SQLite
├── livraria.db               # Banco de dados local SQLite
├── main.py                   # Endpoints da API FastAPI e injeção de dependências
├── models.py                 # Modelos ORM (BookModel e UserModel)
├── schemas.py                # Schemas de validação e serialização do Pydantic
├── requirements.txt          # Dependências do projeto
├── .gitignore                # Arquivos ignorados pelo controle de versão
└── README.md                 # Documentação completa do projeto
```
