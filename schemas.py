from pydantic import BaseModel
from datetime import datetime
from typing import List


class DataBase(BaseModel):
    data: str
    url_id: int


class CreateData(DataBase):
    pass


class DataRead(DataBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True


class UrlBase(BaseModel):
    url: str
    xpath: str
    interval: int


class CreateUrl(UrlBase):
    pass


class UrlRead(UrlBase):
    id: int
    data_list: list[DataRead] = []

    class Config:
        orm_mode = True
