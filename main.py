from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import model
from database import engine, get_db
from schemas import *
from parser import parse_xpath
from datetime import datetime
from requests.exceptions import MissingSchema, HTTPError
import uvicorn

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/begin_parsing/")
def create(details: CreateUrlSchema, db: Session = Depends(get_db)):
    to_create = model.Url(
        url=details.url,
        xpath=details.xpath,
        interval=details.interval
    )
    db.add(to_create)
    db.commit()
    try:
        data = parse_xpath(details.url, details.xpath)
        data_to_add = model.ParseData(
            url_id=to_create.id,
            data=data,
            date=datetime.utcnow()
        )
    except MissingSchema:
        db.delete(to_create)
        db.commit()
        return {
            "success": False,
            'error_message': f'Invalid URL {details.url}'
        }
    except HTTPError:
        db.delete(to_create)
        db.commit()
        return {
            "success": False,
            'error_message': 'Client or server error'
        }

    db.add(data_to_add)
    db.commit()
    return {
        "success": True,
        "created_id": to_create.id,
        "created_data": data_to_add.data
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
