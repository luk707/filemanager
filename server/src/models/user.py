from pydantic import BaseModel, ConfigDict, HttpUrl
from pydantic.alias_generators import to_camel
from datetime import datetime


class User(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    id: str
    created_at: datetime | None = None
    name: str | None = None
    avatar_url: str | None = None
