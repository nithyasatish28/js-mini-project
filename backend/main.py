from fastapi import FastAPI
import functions

app = FastAPI()

@app.get("/complaints")
def get_complaints(status = None,category=None):
    return functions.get_complaints(status=status,category=category)

@app.get("/complaints/{id}")
def get_one_complaint(id:int):
    return functions.get_one_complaint(id=id)

@app.post("/complaints")
def create_complaint(rollno:str, roomno:int, description:str, category:str):
    return functions.update_complaint(rollno=rollno, roomno=roomno, category=category, description=description)

@app.patch("/complaints/{complaint_id}")
def update_complaint_status(complaint_id: int, new_status: str, note: str):
    return functions.update_complaint_status(complaint_id=complaint_id, new_status=new_status, note=note)
