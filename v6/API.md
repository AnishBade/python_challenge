
## Alembic

```shell
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Running FastAPI

```shell
uvicorn api.app:app --reload
```


## Running PostgreSQL container only

```shell
docker-compose -f docker-compose-dev.yml up python-postgresql -d
```

## pre-commit setup

```shell
pip install pre-commit
pre-commit install
```
