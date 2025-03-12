import pytest
from fastapi.testclient import TestClient
from fastapi import status
from src.main import app
from src.repositories.files.fastapi import get_file_repository
from src.repositories.files.base import FileRepository
from minio.error import S3Error


@pytest.fixture
def test_client():
    yield TestClient(app)
    app.dependency_overrides = {}


def test_ready(test_client):
    response = test_client.get("/ready")
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_stat_successful(mocker, test_client):
    mock_file_repository = mocker.MagicMock(
        spec=FileRepository,
    )
    mock_file_repository.stat = mocker.AsyncMock(return_value=[])
    app.dependency_overrides[get_file_repository] = lambda: mock_file_repository

    response = test_client.get(
        "/workspaces/test_workspace_id/stat/some/path",
    )

    mock_file_repository.stat.assert_called_once_with(
        "test_workspace_id",
        "some/path",
    )
    assert response.status_code == status.HTTP_200_OK


def test_stat_failure(mocker, test_client):
    mock_file_repository = mocker.MagicMock(
        spec=FileRepository,
    )
    mock_file_repository.stat = mocker.AsyncMock(
        side_effect=S3Error(None, None, None, None, None, None)
    )
    app.dependency_overrides[get_file_repository] = lambda: mock_file_repository
    response = test_client.get(
        "/workspaces/test_workspace_id/stat/some/path",
    )
    mock_file_repository.stat.assert_called_once_with(
        "test_workspace_id",
        "some/path",
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "404_NOT_FOUND: some/path not found in test_workspace_id"
    }
