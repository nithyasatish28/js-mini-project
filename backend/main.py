from fastapi import FastAPI,HTTPException
import functions

app=FastAPI()


@app.get('/complaints')
def show_complaints():
    return functions.get_all_complaints()


@app.get('/updates/{id}')
def show_complaints_by_id(id):
    return functions.get_complaint(id=id)


@app.get('/complaints/{roll_no}')
def show_complaints(roll_no):
    return functions.get_all_complaints(roll_no=roll_no)


@app.post("/complaints")
def item(roll_no,room_no,category,description):
    return functions.add_lost_item(roll_no=roll_no,category=category,description=description,room_no=room_no)


@app.patch("/Updates/{status}")
def update(id,status, note):
    return functions.Update_complaints(id=id,status=status,note=note )

@app.delete("/complaints")
def delete(id):
    return functions.delete_complaint(id=id)

@app.get('/Update/{status}')
def show_complaints(roll_no):
    return functions.get_all_complaints(roll_no=roll_no)

@app.get("/getbystatus")
def getbystatus():
    status_open = functions.get_complaint_by_status(status="open")
    status_x=[]
    status_y = []
    return {"open":len(status_open), "x":len(status_x)}