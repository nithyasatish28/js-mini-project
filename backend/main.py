from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI(
    title = "Hostel Complaint Tracker API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#E1
@app.get("/complaints")
def all_complaints():
    return functions.get_all_complaints()