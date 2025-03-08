from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from datetime import datetime
from minio.datatypes import Object
from typing import Optional
import mimetypes


class File(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    basename: str
    path: str
    content_type: Optional[str] = "application/octet-stream"
    size: Optional[int] = 0
    last_modified: Optional[datetime]
    is_dir: bool

    @staticmethod
    def from_minio_object(obj: Object) -> "File":
        obj_name = obj.object_name
        return File(
            name=obj_name,
            content_type=obj.content_type
            or mimetypes.guess_file_type(obj.object_name)[0],
            size=obj.size,
            last_modified=obj.last_modified,
            basename=obj_name.split("/")[-1].split(".")[0],
            path="/".join(obj_name.split("/")[:-1])
            if len(obj_name.split("/")) > 1
            else "/",
            is_dir=obj_name.endswith("/"),
        )
