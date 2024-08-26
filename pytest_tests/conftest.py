import json

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils.functions import (
    create_database, database_exists, drop_database
)

from main import APP
from sql_app import models
from sql_app.database import get_db


@pytest.fixture(scope="session")
def test_db_engine():
    sqlalchemy_database_url = "sqlite:///./test_sql_app.db"
    engine = create_engine(
        sqlalchemy_database_url, connect_args={"check_same_thread": False}
    )
    if not database_exists:
        create_database(engine.url)
    models.Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def test_db(test_db_engine):
    connection = test_db_engine.connect()
    connection.begin()
    db = Session(bind=connection)
    yield db
    db.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(test_db):
    APP.dependency_overrides[get_db] = lambda: test_db

    with TestClient(APP) as test_client:
        yield test_client


@pytest.fixture
def json_for_the_post_request():
    message = {
        "monitoring_url": "https://art.com",
        "port": 8080,
        "service": {
            "timeout_ms": 100
        }
    }
    return json.dumps(message)
