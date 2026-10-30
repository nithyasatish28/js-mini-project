from fastapi import FastAPI, HTTPException
import function

app = FastAPI()


@app.on_event("startup")
def startup():
    function.add_initial_stations()


@app.get("/")
def hello():
    return {"message": "Umbrella Sharing API is running"}