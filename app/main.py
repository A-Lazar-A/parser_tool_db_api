from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import model
from app.database import engine, get_db
from app.schemas import *
import uvicorn
from app import crud
from apscheduler.schedulers.background import BackgroundScheduler
from app.parser import parse_xpath

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
scheduler = BackgroundScheduler()


def scheduler_start(sec, url, xpath, url_id):
    scheduler.pause()
    scheduler.add_job(parse_xpath, 'interval', args=(url, xpath, url_id), seconds=sec, id=str(url_id))
    scheduler.resume()


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
    url = crud.add_url(db, details)
    scheduler_start(details.interval, details.url, details.xpath, url.id)
    return url


@app.delete("/delete/{id}")
def delete(id: int, db: Session = Depends(get_db)):
    scheduler.pause()
    scheduler.remove_job(str(id))
    scheduler.resume()
    crud.remove_url(db, id)
    return {"success": True}


if __name__ == "__main__":

    try:
        scheduler.start()
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except (KeyboardInterrupt, SystemExit):

        scheduler.shutdown()
