from fastapi import FastAPI
import AM_functions

app =FastAPI()

@app.get("/plants")
def get_plants():
    return AM_functions.get_all_plants()

