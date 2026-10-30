from fastapi import FastAPI
import functions

app = FastAPI()

@app.get("/complaints")
def get_complaints(status = None,category=None):
    return functions.get_complaints(status=status,category=category)

@app.get("/complaints/{id}")
def get_one_complaint(id:int):
    return functions.get_one_complaint(id=id)