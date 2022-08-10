from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import model
from database import engine, get_db
from schemas import *
import uvicorn
import crud
import os
from apscheduler.schedulers.background import BackgroundScheduler

model.Base.metadata.create_all(bind=engine)

app = FastAPI()
scheduler = BackgroundScheduler()


def scheduler_start(sec, url, xpath, url_id):
    # setting the scheduled task
    scheduler.add_job(job, 'interval', args=(url, xpath, url_id), seconds=sec)

    # starting the scheduled task using the scheduler object


def job(url, xpath, url_id):
    os.system(f'python3 parser.py {url} {xpath} {url_id}')


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


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    scheduler.start()
    try:
        # To simulate application activity (which keeps the main thread alive).
        while True:
            continue
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary but recommended
        scheduler.shutdown()
