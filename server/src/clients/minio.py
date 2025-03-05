from minio import Minio

client = Minio(
    endpoint="127.0.0.1:9000",
    access_key="admin",
    secret_key="password",
    secure=False,
)
