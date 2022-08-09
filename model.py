from sqlalchemy import Integer, String, Interval, DateTime, ForeignKey
from sqlalchemy.sql.schema import Column
from sqlalchemy.orm import relationship
from database import Base


class Url(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    xpath = Column(String, nullable=False)
    interval = Column(Interval, nullable=False)
    data = relationship('ParseData')


class ParseData(Base):
    __tablename__ = 'parse_data'

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer, ForeignKey('urls.id'))
    data = Column(String, nullable=True)
    date = Column(DateTime, nullable=False)
