from datetime import datetime

from fastapi import FastAPI
import functions

app = FastAPI()


@app.patch("/equipments{equipment_id}/status")
def update_service(equipment_id : int, in_service : bool):
    functions.update_service(equipment_id,in_service)
    return {"message": "Equipment status updated successfully."}