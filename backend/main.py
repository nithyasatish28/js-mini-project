from fastapi import FastAPI, HTTPException
import functions

app = FastAPI()

@app.get("/equipment")
def get_equipment_list():
    return functions.get_all_equipment()

@app.get("/equipments/{id}")
def get_equipment_by_id(id: int):
    result = functions.get_equipment(id)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found."
        )
    return result

@app.post("/equipment")
def add_new_item():
    return functions.add_equipment()

@app.patch("/equipment/{id}/service")
def status(id:int,request:ServerRequest):
    result = functions.update_service(
        id=id,
        in_service=request.in_service
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found."
        )
    return result
