from Backend.databaseorm import SessionLocal, Equipment


def add_equipment(name, type, lab_room):

    with SessionLocal() as session:

        equipment = Equipment(
            name=name,
            type=type,
            lab_room=lab_room,
            in_service=1
        )

        session.add(equipment)
        session.commit()
        session.refresh(equipment)

        return {
            "id": equipment.id,
            "name": equipment.name,
            "type": equipment.type,
            "lab_room": equipment.lab_room,
            "in_service": equipment.in_service
        }