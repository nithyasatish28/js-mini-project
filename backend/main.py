# from fastapi import FastAPI,HTTPException
# import functions

# app=FastAPI()


# @app.get('/complaints')
# def show_complaints():
#     return functions.get_all_complaints()


# @app.get('/updates/{id}')
# def show_complaints_by_id(id):
#     return functions.get_complaint(id=id)


# @app.get('/complaints/{roll_no}')
# def show_complaints(roll_no):
#     return functions.get_all_complaints(roll_no=roll_no)


# @app.post("/complaints")
# def item(roll_no,room_no,category,description):
#     return functions.add_lost_item(roll_no=roll_no,category=category,description=description,room_no=room_no)


# @app.patch("/Updates/{status}")
# def update(id,status, note):
#     return functions.Update_complaints(id=id,status=status,note=note )

# @app.delete("/complaints")
# def delete(id):
#     return functions.delete_complaint(id=id)

# @app.get('/Update/{status}')
# def show_complaints(roll_no):
#     return functions.get_all_complaints(roll_no=roll_no)

# @app.get("/getbystatus")
# def getbystatus():
#     status_open = functions.get_complaint_by_status(status="open")
#     status_x=[]
#     return {"open":len(status_open), "x":len(status_x)}


from fastapi import FastAPI, HTTPException
import functions

app = FastAPI()


@app.get("/complaints")
def show_complaints():
    return functions.get_all_complaints()

@app.get("/complaints/counts")
def complaint_counts():
    return functions.get_complaint_counts()


@app.get("/complaints/{complaint_id}")
def show_complaint(complaint_id: int):
    complaint = functions.get_complaint(complaint_id)
    if complaint is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return complaint

@app.post("/complaints", status_code=201)
def add_complaint(roll_no: str, room_no: str, category: str, description: str):

    if category not in ["electrical", "plumbing", "furniture", "cleaning", "internet"]:
        raise HTTPException(status_code=422, detail="Invalid category")
    if len(description.strip()) < 10:
        raise HTTPException(status_code=422, detail="Description is too short")
    result = functions.add_complaint(
        roll_no=roll_no,
        room_no=room_no,
        category=category,
        description=description
    )
    if result is False:
        raise HTTPException(
            status_code=409,
            detail="An unresolved complaint already exists for this room and category")
    return result

@app.patch("/complaints/{complaint_id}/status")
def update_complaint(complaint_id: int, status: str, note: str):
    result = functions.update_complaint(
        complaint_id=complaint_id,
        status=status,
        note=note
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if result is False:
        raise HTTPException(status_code=409, detail="Invalid status change")
    return result

@app.get("/students/{roll_no}/complaints")
def student_complaints(roll_no: str):
    return functions.get_student_complaints(roll_no)


@app.delete("/complaints/{complaint_id}")
def delete_complaint(complaint_id: int):
    result = functions.delete_complaint(complaint_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Complaint not found")
    if result is False:
        raise HTTPException(status_code=409, detail="Only open complaints can be deleted")
    return {"message": "Complaint deleted successfully"}

