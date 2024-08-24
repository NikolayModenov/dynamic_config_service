import json

from fastapi.testclient import TestClient
from main import APP
import pytest


@pytest.fixture
def default_client():
    return TestClient(APP)


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
