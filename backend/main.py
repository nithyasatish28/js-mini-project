from fastapi import FastAPI, HTTPException
import functions

app = FastAPI()


@app.get("/equipment")
def get_equipment():
    return functions.get_all_equipments()