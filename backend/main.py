from API.retrieve import todays_predictions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from flashscore.extract.scrape import FlashscoreApp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from flashscore.predictions.processing import run
from flashscore.outcome.process import update_results
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

app = FastAPI()

origins = [
    "http://localhost:3000", "http://3.109.177.65:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Popup Predicts Home"}


@app.get("/gen-predictions/")  
def get_predictions(day: int | None = 0):
    return todays_predictions(day)


def day_offset():
    now_utc = datetime.utcnow()
    now_ny = now_utc.replace(tzinfo=ZoneInfo("UTC")).astimezone(ZoneInfo("America/New_York"))
    if now_ny.hour >= 0:
        return 1
    return 0

def run_matches():
    flash = FlashscoreApp(concurrency=2)
    flash.start()
    flash.run_app(days=0)    
    flash.stop()
    run()
    flash.start()
    flash.run_app(days=-day_offset())
    flash.stop()
    update_results()



@app.on_event("startup")
def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_matches, CronTrigger(hour=5, minute=15))
    scheduler.start()
