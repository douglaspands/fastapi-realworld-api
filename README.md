# fastapi-realworld-api [EM DESENVOLVIMENTO]
Exemplo de projeto com `FastAPI` e `SQLModel` usando `async/await` utilizado no mundo real.

## Requerimentos
- Python ~3.12
- Poetry ~1.8.0

## Como usar
Seguem os passos para iniciar a aplicação (os passos 1, 2 e 3 precisam ser executados somente na primeira vez).

### 1. Instalar dependencias
Na primeira vez é necessario instalar todas as dependencias executando o seguinte comando:
```sh
poetry install
```

### 2. Criar arquivo .env
```sh
db_url=sqlite+aiosqlite:///database.db
db_debug=1
``` 

### 3. Executar migrações
```sh
poetry run migrate
``` 

### 4. Iniciar aplicação
```sh
poetry run server
```
