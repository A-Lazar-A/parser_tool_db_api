from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import model
from database import engine, get_db
from schemas import *
import uvicorn
import crud

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/read/', response_model=List[UrlRead])
def read_urls(db: Session = Depends(get_db)):
    return crud.get_urls(db)


@app.post("/add_parse_data/", response_model=DataRead)
def add_parse_data(details: CreateData, db: Session = Depends(get_db)):
    return crud.add_url_data(db, details)


@app.post("/begin_parsing/", response_model=UrlRead)
def create(details: CreateUrl, db: Session = Depends(get_db)):
    return crud.add_url(db, details)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
