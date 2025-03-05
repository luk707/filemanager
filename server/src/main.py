from fastapi import FastAPI, UploadFile
from clients.minio import client
from models.file import File
from rich import print
from typing import Optional

app = FastAPI()


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

    # -- for a later date --
    # TODO: Return a union list when listing i.e list[File|Folder] to tell the
    #       client what folders exist in the current path
    # TODO: Use the path option to filter files in a specific path of the bucket
    # TODO: as well a listing of the files in the directory, we should also list
    #       the folders within the directory

    return [File.from_minio_object(obj) for obj in client.list_objects(workspace_id)]


@app.get("/workspaces/{workspace_id}/download/{path:path}")
async def download_file(path: str):
    # TODO: Use this to download files
    #       1. check that there is actually a file at this path
    #       2. stream the content of the file using
    pass


@app.post("/workspaces/{workspace_id}/upload")
async def upload_file(files: list[UploadFile]):
    # TODO: Replace this with the logic to upload a file to the given workspace
    # There may be multiple files in this so you will need to handle all of them
    for file in files:
        # TODO: Perform the upload logic
        print(file)
    # HINT: You can test this logic by using the frontend and uploading a file,
    #       it is already wired up to this endpoint meaning you can use the UI
    #       to test it, the /docs url on the api also provides a way to test
    #       this logic.
    pass


# delete file
@app.delete("/workspaces/{workspace_id}/{path:path}")
async def delete_file(path: str):
    # TODO: Implement logic to delete files from a workspace
    # 1. check that the file path is a valid path to a file or folder
    # 2. perform the deletion logic
    pass
