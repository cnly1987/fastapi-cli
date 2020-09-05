# fastapi-cli
a fastapi Build tool

## setting
* core/database.py
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@127.0.0.1:3306/databasename"

* alembic.ini
sqlalchemy.url = "mysql+pymysql://username:password@127.0.0.1:3306/databasename"

* migrations/env.py
  ++from appcations.users.models import * 
  if you have many models


## cores

* core/crud.py
* core/security.py
* core/serializer.py
* core/cookie.py
* utils/cbv.py

## example
* appcations/users
schemas.py
models.py
crud.py
routers/*




