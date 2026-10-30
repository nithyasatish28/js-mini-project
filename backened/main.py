from fastapi import FastAPI ,HTTPException
import function 
app = FastAPI()

@app.get("/Events")
def events():
    return function.get_all_event(  )