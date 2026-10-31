from fastapi import FastAPI, HTTPException
import functions

app = FastAPI()

@app.get("/complaints")
def get_complaints(status=None, category=None):
    result = functions.get_complaints(status=status, category=category)
    if result is None:
        raise HTTPException(status_code=404, detail="No complaints found")
    return result

@app.get("/complaints/stats/counts")
def get_status_counts():
    return functions.get_complaint_status_counts()

@app.get("/complaints/{id}")
def get_one_complaint(id: int):
    result = functions.get_one_complaint(id=id)
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return result

@app.post("/complaints")
def create_complaint(rollno: str, roomno: int, description: str, category: str):
    return functions.create_complaint(rollno=rollno, roomno=roomno, category=category, description=description)

@app.put("/complaints/{complaint_id}")
def update_complaint(complaint_id: int, status: str, note: str = None):
    result = functions.update_complaint_status(complaint_id=complaint_id, new_status=status, note=note)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/complaints/student/{rollno}")
def get_complaints_by_rollno(rollno: str):
    result = functions.get_students_complaints_byrollno(rollno=rollno)
    if result is None:
        raise HTTPException(status_code=404, detail="No complaints found for this student")
    return result

@app.delete("/complaints/{id}")
def delete_complaint(id: int):
    result = functions.delete_complaint(complaint_id=id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result