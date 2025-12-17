# FastAPI Real World API
Exemplo de projeto com `FastAPI` e `SQLModel` usando `async/await` utilizado no mundo real.   
Meu desejo é apresentar um motor de API REST utilizando o que considero que tem de melhor no universo Python. `[MINHA OPINIÃO]`   
Conforme vou adquirindo mais conhecimento, vou ajustando o projeto para ficar mais claro. 

## Requerimentos
- Python >=3.12
- Poetry >=2.0

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
- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Qualidade
Para executar os comandos a seguir, é necessario ter as [dependencias instaladas](#1-instalar-dependencias).

### Validação de código (Linter)
```sh
poetry run lint
```

### Testes unitarios
```sh
poetry run unit_test
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
docker exec -it api-container bash -c 'DB_ROOT_URL="postgresql+psycopg://postgres:docker@db-service:5432/fastapi" alembic upgrade head'
```

## Kubernetes

Os manifestos deste projeto foram desenvolvidos e testados utilizando [microK8s](https://microk8s.io/).

### Iniciando todas as instancias
```sh
kubectl apply -k k8s
```

### Preparando o banco de dados
Criar um `port-forward` para acessar o banco de dados:
```sh
kubectl -n realworld port-forward pod/db-deploy 5432:5432
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

Executar os scripts de migração do banco de dados:
```sh
kubectl -n realworld exec pod/api-deploy -- bash -c 'DB_ROOT_URL="postgresql+psycopg://postgres:docker@db-service.realworld.svc.cluster.local:5432/fastapi" alembic upgrade head'
```


## Dicas

### DNS
```yaml
api: api-service.realworld.svc.cluster.local:8080
db: db-service.realworld.svc.cluster.local:5432
```

### MicroK8s? Serviços que precisam ser iniciados
```sh
microk8s enable dashboard
microk8s enable dns
microk8s enable registry
microk8s enable ingress
```

### Verificar DNS da API
```sh
kubectl -n realworld run mycurlpod --image=curlimages/curl -i --tty -- sh
```
execute o comando:
```sh
curl -i http://api-service.realworld.svc.cluster.local:8080/docs
```

## Changelog
Todas as notas de alteração deste projeto serão documentados no [CHANGELOG.md](./CHANGELOG.md).
