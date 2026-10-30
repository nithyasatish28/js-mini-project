from Backend.databaseorm import SessionLocal, Equipment


def get_equipment_by_id(equipment_id):
    with SessionLocal() as session:
        equipment = session.get(Equipment, equipment_id)

        if equipment is None:
            return None

        return {
            "id": equipment.id,
            "name": equipment.name,
            "type": equipment.type,
            "lab_room": equipment.lab_room,
            "in_service": equipment.in_service,
        }