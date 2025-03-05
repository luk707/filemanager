from fastapi import FastAPI
from clients.minio import client

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/files")
async def list_files(name_of_bucket):
    return client.list_objects(name_of_bucket)


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
