from fastapi import FastAPI
import functions

app = FastAPI()

@app.get("/complaints")
def get_complaints(status = None,category=None):
    return functions.get_complaints(status=status,category=category)