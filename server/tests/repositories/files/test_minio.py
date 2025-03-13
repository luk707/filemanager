import pytest
from minio import Minio
from minio.datatypes import Object
from minio.error import S3Error
from src.models.file import directory_listing_from_object
from src.repositories.files.minio import MinioFileRepository


@pytest.fixture
def test_client(mocker):
    yield mocker.MagicMock(spec=Minio)


@pytest.mark.asyncio
async def test_stat_successful(
    mocker,
    test_client,
):
    mock_reponse = [
        Object(
            bucket_name="test_workspace_id",
            object_name="some/path/test_file.txt",
            size=100,
            last_modified="2021-10-01T12:00:00Z",
            content_type="text/plain",
        ),
        Object(
            bucket_name="test_workspace_id",
            object_name="some/path/subdir/",
            size=0,
            last_modified="2021-10-01T12:00:00Z",
        ),
    ]
    test_client.list_objects = mocker.MagicMock(return_value=mock_reponse)
    repository = MinioFileRepository(test_client, None)
    response = await repository.stat("test_workspace_id", "some/path")
    test_client.list_objects.assert_called_once_with(
        "test_workspace_id", prefix="some/path/"
    )
    assert response == [
        directory_listing_from_object(obj)
        for obj in mock_reponse
        if obj.object_name != "some/path/"
    ]


@pytest.mark.asyncio
async def test_stat_failure(
    mocker,
    test_client,
):
    test_client.list_objects = mocker.MagicMock(
        side_effect=S3Error(
            None,
            None,
            None,
            None,
            None,
            None,
        )
    )
    repository = MinioFileRepository(test_client, None)
    with pytest.raises(S3Error):
        await repository.stat("test_workspace_id", "some/path")
        test_client.list_objects.assert_called_once_with(
            "test_workspace_id", prefix="some/path/"
        )
