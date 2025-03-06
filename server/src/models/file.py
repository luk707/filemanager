from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from datetime import datetime
from minio.datatypes import Object
import mimetypes


class File(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    name: str
    content_type: str = "application/octet-stream"
    size: int
    last_modified: datetime

    @staticmethod
    def from_minio_object(obj: Object) -> "File":
        return File(
            name=obj.object_name,
            content_type=obj.content_type
            or mimetypes.guess_file_type(obj.object_name)[0],
            size=obj.size,
            last_modified=obj.last_modified,
        )
