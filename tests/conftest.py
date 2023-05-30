from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import config
from app.database import get_db
from app.database import Base
import pytest


db_host = config.db_host.get_secret_value()
db_name = config.db_name.get_secret_value()
db_user = config.db_user.get_secret_value()
db_pass = config.db_pass.get_secret_value()
db_port = config.db_port.get_secret_value()

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (db_user, db_pass, db_host, db_port, db_name)
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
