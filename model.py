from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship
from database import Base


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    xpath = Column(String, nullable=False)
    interval = Column(Integer, nullable=False)
    data_list = relationship('ParseData', cascade="all,delete",  back_populates="parsing_url")


class ParseData(Base):
    __tablename__ = 'parse_data'

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'))
    data = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
    parsing_url = relationship('Url',  back_populates="data_list")
