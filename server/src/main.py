from fastapi import FastAPI
from clients.minio import client
from models.file import File

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/workspace/{workspace_id}")
async def list_files(workspace_id: str) -> list[File]:
    return [File.from_minio_object(obj) for obj in client.list_objects(workspace_id)]


@app.post("/files")
async def upload_file():
    # Code to upload files will go here
    pass


# delete file
@app.delete("/files/{file_path:path}")
async def delete_file(file_path: str):
    # Code to delete files will go here
    pass


# download file
@app.get("/files/{file_path:path}")
async def download_file(file_path: str):
    # Code to download files will go here
    pass
