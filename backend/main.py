from fastapi import FastAPI , HTTPException
import functions

app = FastAPI()

@app.get("/complaints")
def get_complaints(status = None,category=None):
    if not functions.get_complaints(status=status,category=category):
        raise HTTPException(status_code=404,detail="No Complaint found")
    return functions.get_complaints(status=status,category=category)

@app.get("/complaints/{id}")
def get_one_complaint(id:int):
    if not functions.get_one_complaint(id=id):
        raise HTTPException(status_code=404 , detail="ID not found")
    return functions.get_one_complaint(id=id)

@app.post("/complaints")
def create_complaint(rollno:str, roomno:int, description:str, category:str):
    return functions.create_complaint(rollno=rollno, roomno=roomno, category=category, description=description)

@app.patch("/complaints/{complaint_id}")
def update_complaint_status(complaint_id: int, new_status: str, note: str):
    return functions.update_complaint_status(complaint_id=complaint_id, new_status=new_status, note=note)


@app.get("/complaints/students/{rollno}")
def get_complaints_by_rollno(rollno: str):
    return functions.get_complaints_by_rollno(rollno=rollno)