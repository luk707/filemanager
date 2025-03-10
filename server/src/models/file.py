from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from datetime import datetime
from minio.datatypes import Object
import mimetypes
from enum import Enum
from typing import Annotated, Literal, Union
import os


class DirectoryListingType(str, Enum):
    FILE = "file"
    DIRECTORY = "directory"


class File(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal[DirectoryListingType.FILE] = DirectoryListingType.FILE

    name: str
    basename: str
    path: str
    content_type: str
    size: int
    last_modified: datetime


class Directory(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    type: Literal[DirectoryListingType.DIRECTORY] = DirectoryListingType.DIRECTORY

    name: str
    path: str


DirectoryListing = Annotated[
    Union[File, Directory],
    Field(discriminator="type"),
]


def directory_listing_from_object(obj: Object) -> DirectoryListing:
    if obj.object_name.endswith("/"):
        return Directory(
            name=os.path.basename(obj.object_name[:-1]),
            path=obj.object_name[:-1],
        )

    return File(
        name=obj.object_name,
        content_type=obj.content_type
        or mimetypes.guess_file_type(obj.object_name)[0]
        or "application/octet-stream",
        size=obj.size,
        last_modified=obj.last_modified,
        basename=os.path.basename(obj.object_name),
        path=os.path.split(obj.object_name)[0],
    )
