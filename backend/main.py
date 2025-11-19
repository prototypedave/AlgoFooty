from API.retrieve import todays_predictions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from flashscore.extract.scrape import FlashscoreApp
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
#from flashscore.predictions.processing import run
#from flashscore.outcome.process import update_results

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"Popup Predicts Home"}


@app.get("/gen-predictions/")  
async def get_predictions(day: int | None = 0):
    return todays_predictions(day)
    
'''
async def run_matches():
    flash = FlashscoreApp(concurrency=2)
    await flash.start()
    await flash.run_app(days=0)    
    await flash.stop()
    run()
    await flash.start()
    await flash.run_app(days=-1)
    await flash.stop()
    update_results()


@app.on_event("startup")
async def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(run_matches, CronTrigger(hour=0, minute=0))
    scheduler.start()'''