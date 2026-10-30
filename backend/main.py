from fastapi import FastAPI,HTTPException
import functions

app=FastAPI()


@app.get('/complaints')
def show_complaints():
    return functions.get_all_complaints()


@app.post("/complaints")
def item(roll_no,room_no,category,description):
    return functions.get_complaint(roll_no=roll_no,description=description,room_no=room_no)


