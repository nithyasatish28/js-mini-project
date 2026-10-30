from Backend.databaseorm import SessionLocal, Equipment
def get_all_equipment():
    #	Get all the equipment. Can be filtered by type.
    session = SessionLocal()

    equipment_list = session.query(Equipment).all()
    session.close()

    return equipment_list

def get_equipment_by_type(equipment_type):
    session = SessionLocal()
    equipment_list = session.query(Equipment).filter(
        Equipment.type == equipment_type
    ).all()
    session.close()
    return equipment_list