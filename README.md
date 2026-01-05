# FastAPI Real World API
Exemplo de projeto com `FastAPI` e `SQLModel` usando `async/await` utilizado no mundo real.   
Meu desejo é apresentar um motor de API REST utilizando o que considero que tem de melhor no universo Python. `[MINHA OPINIÃO]`   
Conforme vou adquirindo mais conhecimento, vou ajustando o projeto para ficar mais claro. 

## Requerimentos
- Python >=3.13
- uv >=0.9

## Como usar
Segue abaixo os passos para iniciar a aplicação.
> Passos 1, 2 e 3 precisam ser executados somente na primeira vez.

### 1. Instalar dependencias
Na primeira vez é necessario instalar todas as dependencias executando o seguinte comando:
```sh
uv sync
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
uv run migrate
``` 

### 4. Iniciar aplicação
Iniciar a aplicação (modo `watch`):
```sh
uv run server
```
Após iniciado, o `OpenAPI Specification` da aplicação estará disponivel em 2 endpoints:
- [http://localhost:8000/docs](http://localhost:8000/docs)
- [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Qualidade
Para executar os comandos a seguir, é necessario ter as [dependencias instaladas](#1-instalar-dependencias).

### Validação de código (Linter)
```sh
uv run lint
```

### Testes unitarios
```sh
uv run unit_test
``` 

### Build
```sh
uv run build
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

Os manifestos deste projeto foram desenvolvidos e testados utilizando o **KinD**.

### KinD

Para rodar o K8s localmente, é necessario a instalação:
1. Instalar o [KinD](https://kind.sigs.k8s.io/docs/user/quick-start/);
2. Instalar o [kubectl](https://kubernetes.io/pt-br/docs/tasks/tools/)
3. Instalar o [LoadBalancer](https://github.com/kubernetes-sigs/cloud-provider-kind);

Eu instalei tudo usando o gerenciador de pacotes [brew](https://brew.sh):
```sh
brew install kind cloud-provider-kind kubectl
``` 
Agora execute os seguintes procedimentos:
1. Inicie o LoadBalancer:

```sh
cloud-provider-kind --gateway-channel standard
```
> Iniciar em um terminal isolado.

2. Criar o [cluster com docker registry](https://kind.sigs.k8s.io/docs/user/local-registry/):
```sh
./scripts/kind-with-registry.sh
```
> Caso queria encerrar o cluster: `kind delete cluster`.


### Publicando a imagem da aplicação no registry local
Para o manifesto do Kubernetes conseguir iniciar a aplicação, a imagem docker precisa estar no registry local.
Para isso minha recomendação é criar a imagem com o `docker-compose`:
```sh
docker compose build
```
Publicar a imagem no registry local:
```sh
docker compose push
```

### Iniciando todas as instancias
```sh
kubectl apply -k k8s
```

### Preparando o banco de dados
Criar um `port-forward` para acessar o banco de dados:
```sh
kubectl -n realworld port-forward deployments/db-deploy 5432:5432
```

Com sua IDE favorita do `PostgreSQL`, execute os seguintes comandos:
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
kubectl -n realworld exec deployments/api-deploy -- bash -c 'DB_ROOT_URL="postgresql+psycopg://postgres:docker@db-service.realworld.svc.cluster.local:5432/fastapi" alembic upgrade head'
```

## Dicas e Orientações

### DNS
```yaml
api: api-service.realworld.svc.cluster.local:8080
db: db-service.realworld.svc.cluster.local:5432
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
