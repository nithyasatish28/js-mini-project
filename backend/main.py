from fastapi import FastAPI, HTTPException
import function
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.get("/")
def hello():
    return ("message : Stations running succussfully")

app.add_middleware(
    CORSMiddleware,
    allow_origins =["http://localhost:5174","http://127.0.0.1:5174"],
    allow_methods =["*"],
    allow_headers =["*"],
)

@app.get("/stations")
def get_stations():
    return function.get_all_stations()

@app.post("/add_stations")
def add_stations(name, capacity:int, umbrellas_available:int, location = None):
    if capacity < 1 or capacity >100 :
        raise HTTPException(status_code=422,detail="capacity between 1-100")
    if umbrellas_available < 0 or umbrellas_available > capacity:
        raise HTTPException(status_code=422,detail="starting umbrellas between 0 and capcity")
        
    return function.add_stations(name=name, capacity=capacity, umbrellas_available = umbrellas_available, location=location)

@app.get("/stations/id")
def station_id(id):
    if function.get_station_by_id(id= id) is None:
        raise HTTPException(status_code=404 ,detail="station not found")
    return function.get_station_by_id(id=id)


@app.post("/borrow/roll_no")
def borrow_umbrella__with_rollno(roll_no,id):
    if not roll_no:
        raise HTTPException(status_code=422,detail="roll no id nedded")
    if not id:
        raise HTTPException(status_code=422,detail="station id needed")
    
    station = function.get_station_by_id(id=id)

    if station["umbrellas_available"]==0:
        raise HTTPException(status_code=409,detail="This station is empty")

    return function.borrow_umbrella_station(roll_no=roll_no,id=id)

@app.patch("/borrow/{roll_no}/return_no")
def retrun_umbrella_no(roll_no,id):
    if not roll_no:
            raise HTTPException(status_code=422,detail="roll no id nedded")
    if not id:
            raise HTTPException(status_code=422,detail="station id needed")
        
    station = function.get_station_by_id(id=id)

    if station is None:
        raise HTTPException(status_code=404, detail="id does not exist.")
        

    if station["capacity"] == station["umbrellas_available"]:
        raise HTTPException(status_code=409,detail="This station is full. Try another one.")
    
    return function.return_umbrella_station(roll_no=roll_no,id=id)

@app.get("/students/returned")
def get_student_unreturned_umbrella(roll_no):
     
     if not roll_no:
        raise HTTPException(status_code=422,detail="roll number is required.")

     if function.get_unreturned_umbrella_by_roll(roll_no=roll_no) is None:
        raise HTTPException(status_code=404,detail="No  umbrella found for this student.")

     return function.get_unreturned_umbrella_by_roll(roll_no=roll_no)
    


@app.get("/stations/attention")
def get_stations_need_attention():
 return function.get_stations_need_attention()



