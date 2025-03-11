import pytest
from fastapi.testclient import TestClient
from fastapi import status
from src.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


def test_ready(test_client):
    response = test_client.get("/ready")
    assert response.status_code == status.HTTP_204_OK
