# fastapi-realworld-api
Exemplo de projeto com `FastAPI` e `SQLModel` usando `async/await` utilizado no mundo real.   
Meu desejo é apresentar um motor de API REST utilizando o que considero que tem de melhor no universo Python. `[MINHA OPINIÃO]`

## Requerimentos
- Python ~3.12
- Poetry ~1.8.0

## Como usar
Segue abaixo os passos para iniciar a aplicação.
> Passos 1, 2 e 3 precisam ser executados somente na primeira vez.

### 1. Instalar dependencias
Na primeira vez é necessario instalar todas as dependencias executando o seguinte comando:
```sh
poetry install
```

### 2. Criar arquivo .env
Criar o arquivo `.env` na raiz do projeto com:
```sh
db_url=sqlite+aiosqlite:///database.db
db_debug=1
``` 

### 3. Executar migrações
Preparar o banco de dados para o uso:
```sh
poetry run migrate
``` 

### 4. Iniciar aplicação
Iniciar a aplicação (modo `watch`):
```sh
poetry run server
```
Após iniciado, o `OpenAPI Specification` da aplicação estará disponivel em 2 endpoints:
- [http://localhost:5000/docs](http://localhost:5000/docs)
- [http://localhost:5000/redoc](http://localhost:5000/redoc)

## Changelog

Todas as notas de alteração deste projeto serão documentados no [CHANGELOG.md](./CHANGELOG.md).
