from pydantic import BaseModel, Field
from datetime import timedelta, datetime


class DataSchema(BaseModel):
    data: str
    date: datetime


class UrlSchema(BaseModel):
    id: int
    url: str
    xpath: str
    interval: timedelta
    data: DataSchema = Field(...)


class CreateUrlSchema(BaseModel):
    url: str
    xpath: str
    interval: timedelta
