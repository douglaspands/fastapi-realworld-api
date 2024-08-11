# fastapi-realworld-api [EM DESENVOLVIMENTO]
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
token_secret_key=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
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

## Qualidade
Para executar os comandos a seguir, é necessario ter as [dependencias instaladas](#1-instalar-dependencias).

### Validação de código (Linter)
```sh
poetry run lint
```

### Testes unitarios
```sh
poetry run test
``` 

### Build
```sh
poetry run build
```
> São executados: [validação de codigo](#validação-de-código-linter) e [testes unitarios](#testes-unitarios).

## Docker-Compose
Iniciar a aplicação com o comando:
```sh
docker compose up
```
| Será feito o build caso seja a primeira vez.

Executar os scripts de `migração` com o seguinte comando:
```sh
docker exec -it fastapi-realword-api bash -c 'DB_ROOT_URL="postgresql+psycopg://postgres:docker@fastapi-realword-db:5432/fastapi" alembic upgrade head'
```

## Kubernetes
Os manifestos deste projeto foram desenvolvidos e testados utilizando [microK8s](https://microk8s.io/).

### Namespaces
```sh
kubectl create namespace realworld
```

### Iniciar
1. Criar namespace:
```
kubectl apply -f k8s/common
```
2. Criar e configurar o banco de dados:
```
kubectl apply -f k8s/db
```
Assim que o banco estiver ativo, criar um `port-forward` para acessar o banco de dados:
```sh
kubectl -n realworld port-forward pod/postgres-pod 5432:5432
```
Com sua IDE favorita do Postgres, execute os seguintes comandos:
```sql
CREATE DATABASE fastapi;
CREATE USER fastapi_user WITH PASSWORD '123456';
GRANT CONNECT ON DATABASE fastapi TO fastapi_user;
GRANT USAGE ON SCHEMA public TO fastapi_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO fastapi_user;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO fastapi_user;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO fastapi_user;
```

3. Iniciar API:
```
kubectl apply -f k8s/api
```

### DNS
#### API
```sh
fastapi-service.realworld.svc.cluster.local:5000
```
| <service-name>.<namespace>.svc.cluster.local:<port>/persons/v1/persons/1

#### DB
```sh
postgres-service.realworld.svc.cluster.local:5432
```

## Changelog
Todas as notas de alteração deste projeto serão documentados no [CHANGELOG.md](./CHANGELOG.md).
