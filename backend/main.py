from API.retrieve import todays_predictions
from fastapi import FastAPI

app = FastAPI()
@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/gen_predictions/")  
async def get_predictions(day: int | None = 0):
    return todays_predictions(day)
    