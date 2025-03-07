import io
import os
from typing import Optional

from clients.minio import client
from fastapi import FastAPI, HTTPException, Response, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from minio.error import S3Error
from models.file import File
from rich import print

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/workspaces/{workspace_id}/stat")
@app.get("/workspaces/{workspace_id}/stat/{path:path}")
async def stat(workspace_id: str, path: Optional[str] = "") -> list[File]:
    # TODO: Check if the path is a file or a directory, or root (i.e. path = "")
    # 1. if path is a file, we should provide information on the specific file
    #    by returning a single File

    # 2. if the path is a directory or root, we should instead return a
    #    directory listing for the client to display, i.e. a list[File]

    if path:
        try:
            response = [
                File.from_minio_object(obj)
                for obj in client.list_objects(workspace_id)
                if obj.object_name == path
            ]
            if response == []:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
                )
            return [
                File.from_minio_object(obj)
                for obj in client.list_objects(workspace_id)
                if obj.object_name == path
            ]
        except S3Error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
            )

    try:
        return [
            File.from_minio_object(obj)
            for obj in client.list_objects(workspace_id, prefix=path)
        ]
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )

    # -- for a later date --
    # TODO: as well a listing of the files in the directory, we should also list
    #       the folders within the directory
    # TODO: Return a union list when listing i.e list[File|Folder] to tell the
    #       client what folders exist in the current path
    # TODO: Use the path option to filter files in a specific path of the bucket

    # TODO: Check user has read permission for workspace

    # is this not moot? it'll be handled by whatever access keygiven to the  client; no? @see clients/minio.py

@app.get("/workspaces/{workspace_id}/download/{path:path}")
async def download_file(workspace_id: str, path: str):
    if not path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )
    try:
        object = client.stat_object(workspace_id, path)
        response = client.get_object(workspace_id, path)
        file_content = b"".join(
            chunk for chunk in response.stream()
        )  # retrieves all chunks and combines them.
        filename = os.path.basename(path)  # gets the filename from the path.

        return Response(
            content=file_content,
            media_type=object.content_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )


@app.post("/workspaces/{workspace_id}/upload")
async def upload_file(workspace_id: str, files: list[UploadFile]):
    # TODO: Replace this with the logic to upload a file to the given workspace
    # There may be multiple files in this so you will need to handle all of them
    # -- for a later date --

    for file in files:
        # TODO: Perform the upload logic

        file_stream = io.BytesIO(await file.read())
        client.put_object(
            workspace_id,
            file.filename,
            file_stream,
            length=file.size,
            content_type=file.content_type,
        )

        # HINT: You can test this logic by using the frontend and uploading a
        #       file, it is already wired up to this endpoint meaning you can
        #       use the UI to test it, the /docs url on the api also provides a
        #       way to test this logic.

        # TODO: Check user has write permission for workspace
        # see @stat()

        print(file)
    pass


# delete file
@app.delete("/workspaces/{workspace_id}/remove/{path:path}")
async def delete_file(workspace_id: str, path: str):
    # TODO: Implement logic to delete files from a workspace
    # 1. check that the file path is a valid path to a file or folder
    try:
        client.stat_object(workspace_id, path)
    except S3Error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: {path} not found in {workspace_id}",
        )
    # 2. perform the deletion logic

    client.remove_object(workspace_id, path)
    return {"message": f"DELETED {path} from {workspace_id}"}

    # -- for a later date --
    # TODO: Check user has write permission for workspace
    # see @stat()
