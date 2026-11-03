# Sistema de Livraria Online - FastAPI & SQLAlchemy

API REST desenvolvida com FastAPI para gerenciamento de livros, integrada a um banco de dados SQLite utilizando SQLAlchemy e versionamento de banco com Alembic.

---

## 🛠️ Tecnologias Utilizadas

- **[Python 3.10+](https://www.python.org/)**
- **[FastAPI](https://fastapi.tiangolo.com/)**: Framework web moderno e de alta performance.
- **[SQLAlchemy](https://www.sqlalchemy.org/)**: ORM para mapeamento objeto-relacional e comunicação com SQLite.
- **[Alembic](https://alembic.sqlalchemy.org/)**: Ferramenta de migração de banco de dados.
- **[Pydantic](https://docs.pydantic.dev/)**: Validação e serialização de dados.
- **[Uvicorn](https://www.uvicorn.org/)**: Servidor ASGI.

---

## 🚀 Como Executar o Projeto Localmente

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
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

Para criar o banco de dados SQLite local (`livraria.db`) e a tabela de livros:

```bash
alembic upgrade head
```

### 5. Iniciar o servidor

```bash
uvicorn main:app --reload
```

A API estará rodando em: `http://127.0.0.1:8000`

---

## 📖 Documentação da API

Após iniciar o servidor, você pode acessar a documentação interativa gerada automaticamente pelo Swagger:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📌 Rotas da API (CRUD de Livros)

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/` | Mensagem de boas-vindas |
| `POST` | `/books/` | Cadastra um novo livro |
| `GET` | `/books/` | Lista todos os livros cadastrados |
| `GET` | `/books/{book_id}` | Obtém detalhes de um livro por ID |
| `PUT` | `/books/{book_id}` | Atualiza os dados de um livro por ID |
| `DELETE` | `/books/{book_id}` | Remove um livro por ID |

---

## 📁 Estrutura do Projeto

```text
├── alembic/              # Diretório de migrações do Alembic
│   ├── versions/         # Arquivos de migração gerados
│   └── env.py            # Configuração do ambiente do Alembic
├── alembic.ini           # Configurações do Alembic
├── database.py           # Configuração do SQLAlchemy e sessão do banco
├── models.py             # Modelos de tabelas do banco de dados (SQLAlchemy)
├── schemas.py            # Modelos de validação e serialização (Pydantic)
├── main.py               # Rotas e regras de negócio da API FastAPI
├── requirements.txt      # Dependências do projeto
├── .gitignore            # Arquivos e diretórios ignorados pelo Git (*.db, venv, etc.)
└── README.md             # Instruções de execução do projeto
```
