from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import model
from database import engine, get_db
from schemas import *

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
    return {
        "success": True,
        "created_id": to_create.id
    }
