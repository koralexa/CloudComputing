from re import sub

from pydantic import BaseConfig, BaseModel, Field

BaseConfig.allow_population_by_field_name = True


def to_camel(s: str) -> str:
    s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
    return "".join([s[0].lower(), s[1:]])


class Detail(BaseModel):
    detail: str


class BookInfo(BaseModel):
    name: str = Field(max_length=100)
    author: str = Field(max_length=50)

    class Config:
        alias_generator = to_camel


class Book(BookInfo):
    id: int
    quantity: int
