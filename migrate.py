import os

os.system('alembic revision --autogenerate -m "init db"')
os.system('alembic upgrade head')