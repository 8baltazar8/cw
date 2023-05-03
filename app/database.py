from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .settings import config

db_host = config.db_host.get_secret_value()
db_name = config.db_name.get_secret_value()
db_user = config.db_user.get_secret_value()
db_pass = config.db_pass.get_secret_value()


SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s/%s" % (db_user, db_pass, db_host, db_name)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
