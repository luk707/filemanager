from fastapi import FastAPI
from clients.minio import client
from models.file import File

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/workspace/{bucket_name}")
async def list_files(bucket_name: str) -> list[File]:
    return [File.from_minio_object(obj) for obj in client.list_objects(bucket_name)]


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
