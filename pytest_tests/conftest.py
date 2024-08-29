import json

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy_utils.functions import create_database, database_exists

from main import APP
from sql_app import models
from sql_app.database import get_db
from sql_app.models import Patch


@pytest.fixture(scope="session")
def test_db_engine():
    sqlalchemy_database_url = "sqlite:///./sql_db_for_tests.db"
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
def dict_for_the_post_request():
    return {
        "monitoring_url": "https://asrt.com",
        "port": 8280,
        "service": {
            "timeout_ms": 111
        }
    }


@pytest.fixture
def bad_dict_for_the_post_request():
    return {
        "mmonitoring_url": "https://asrt.com",
        "port": 8280,
        "service": {
            "timeout_ms": 111
        }
    }


@pytest.fixture
def patch_dicts():
    return [
        {
            "monitoring_url": "https://art.com",
            "port": 8080,
            "service": {
                "timeout_ms": 212
            }
        },
        {"port": 8081},
        {"monitoring_url": ""}
    ]


@pytest.fixture
def much_patches(client, test_db, patch_dicts):
    patches = []
    for patch_dict in patch_dicts:
        jsoned_dict = json.dumps(patch_dict)
        patches.append(Patch(patch=jsoned_dict))
    test_db.add_all(patches)
    test_db.commit()

@pytest.fixture
def patch_content():
    return {"monitoring_url": "https://new.com"}
