# Getting Stated

## Install

- docker on your local machine
- vscode
    - extension `Remote-Containers`

## open with vscode with docker container

open vscode

press `f1` and search `Remote-Containers: Open Folder in Container`

open project file, then start docker container automatically

## debug run

press `f5` on vscode

and access `http://localhost:8000/docs` from browser on local machine


## connect postgres in container from client machine

run `docker exec -it [postgres container name or id] /bin/bash`

`psql -U postgres`
`alter role postgres with password 'postgres'`
`\q`
`exit`

and connect like `postgres://postgres:postgres@localhost:5432/postgres`
with DBeaver, A5, PGAdmin4 and so on


# Migrate DB

`alembic` による Database Migration ができる。

## Model の作成

`app/models` 配下に Database Model を作成する

```python
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")

```

## Model を Alembic の対象にする

Model を追加した場合、 `app/db/base.py` に対象の `import` を追加する

```python
from app.models.user import User  # noqa
```

## Revision の発行

alembic で migrate 情報を自動生成する。
これはローカル上で実行されるだけ

`alembic revision --autogenerate -m "some message"`

## Migrate の実行

以下を発行すると Database に Migration が実行され、table 等に反映される

`alembic upgrade head`
