import pytest
from fastapi.testclient import TestClient
from fastapi import status
from src.main import app
from src.repositories.files.fastapi import get_file_repository
from src.repositories.files.base import FileRepository
from minio.error import S3Error
from src.models.file import File, Directory
from datetime import datetime
from fastapi.encoders import jsonable_encoder


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
    mock_response = [
        File(
            name="some/path/test_file.txt",
            basename="test_file.txt",
            path="some/path",
            content_type="text/plain",
            size=100,
            last_modified=datetime.now(),
        ),
        Directory(
            name="some/path/subdir/",
            path="some/path",
        ),
    ]
    mock_file_repository.stat = mocker.AsyncMock(return_value=mock_response)
    app.dependency_overrides[get_file_repository] = lambda: mock_file_repository
    response = test_client.get(
        "/workspaces/test_workspace_id/stat/some/path",
    )
    mock_file_repository.stat.assert_called_once_with(
        "test_workspace_id",
        "some/path",
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == jsonable_encoder(mock_response)


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
