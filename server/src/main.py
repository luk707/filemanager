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
        objects = list(client.list_objects(workspace_id, prefix=path))
        directories = [File.from_minio_object(obj) for obj in objects if obj.is_dir]
        files = [File.from_minio_object(obj) for obj in objects if not obj.is_dir]
        return directories + files
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


@app.post("/workspaces/{workspace_id}/upload/{directory_path}")
async def upload_file(workspace_id: str, files: list[UploadFile],directory_path:str):
    # TODO: Replace this with the logic to upload a file to the given workspace
    # There may be multiple files in this so you will need to handle all of them
    # -- for a later date --
    for file in files:
        path = directory_path + '/' + file.filename if directory_path else file.filename
        # TODO: Perform the upload logic

        file_stream = io.BytesIO(await file.read())
        client.put_object(
            workspace_id,
            path,
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


@app.get("/workspaces/{workspace_id}/directory/{directory_path}")
async def create_directory(workspace_id: str, directory_path: str):
  empty_data = bytes()
  data_stream = io.BytesIO(empty_data)
  client.put_object(
    workspace_id,
    directory_path+"/",
    data=data_stream,
    length=0,
    content_type="application/octet-stream"
  )
  return {"message": f"CREATED {directory_path} in {workspace_id}"}


@app.delete("/workspaces/{workspace_id}/directory/{directory_path}")
async def delete_directory(workspace_id: str, directory_path: str):

    try:
      objects = list(client.list_objects(workspace_id, prefix=directory_path +"/"))
      
      if len(objects) == 1 and objects[0].object_name == directory_path + "/":
          client.remove_object(workspace_id, directory_path +"/")
          return {"message": f"DELETED {directory_path} in {workspace_id}"}

      for obj in objects:
          client.remove_object(workspace_id, obj.object_name)
          return {"message": f"DELETED {directory_path} from {workspace_id}"}
        
    except S3Error:
      raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"404_NOT_FOUND: dir {directory_path} not found in {workspace_id}",
        )