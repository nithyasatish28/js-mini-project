from fastapi import FastAPI ,HTTPException
import function 
app = FastAPI()

@app.get("/Events")
def events():
    return function.get_all_event(  )



@app.get ("/Events")
def events(id):
    return function.get_all_event() 