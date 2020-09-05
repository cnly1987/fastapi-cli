import uuid

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@127.0.0.1:3306/databasename"
# 注意,如果你用pymysql连接的话，mysql+mysqlconnector:改成mysql+pymsql:

engine = create_engine( SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#返回UUID字符函数，用来给模型默认UUID字段的
def generate_uuid():
    return str(uuid.uuid4())

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
