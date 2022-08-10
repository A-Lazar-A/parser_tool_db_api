from sqlalchemy.orm import Session
import model
import schemas
from datetime import datetime


def get_urls(db: Session):
    return db.query(model.Url).all()


def add_url(db: Session, url_input: schemas.CreateUrl):
    db_url = model.Url(
        url=url_input.url,
        xpath=url_input.xpath,
        interval=url_input.interval,
    )
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url


def add_url_data(db: Session, data_input: schemas.CreateData):
    db_data = model.ParseData(
        data=data_input.data,
        date=datetime.utcnow(),
        url_id=data_input.url_id
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def add_incorrect_url_data(db: Session, data: str, url_id: int):
    db_data = model.ParseData(
        data=data,
        date=datetime.utcnow(),
        url_id=url_id
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
