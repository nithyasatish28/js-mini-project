from datetime import datetime
from functions import Session, engine, Complaints, Updates

rows = [
    ("011", "101", "internet", "Wifi keeps disconnecting every hour", "resolved"),
    ("012", "102", "electrical", "Fan in the room is not working", "resolved"),
    ("013", "103", "plumbing", "Tap in the bathroom is leaking", "open"),
    ("014", "104", "furniture", "Study table leg is broken", "open"),
    ("015", "105", "cleaning", "Corridor has not been cleaned for days", "in_progress"),
    ("016", "106", "electrical", "Tube light flickers all night", "in_progress"),
    ("017", "107", "plumbing", "No water supply on the third floor", "resolved"),
    ("018", "108", "internet", "Router in the common room is down", "open"),
]

session = Session(engine)

# just to clear the old data first that we had add while testing if it worked or not 
session.query(Updates).delete()
session.query(Complaints).delete()

for roll, room, category, description, status in rows:
    complaint = Complaints(
        roll_no=roll,
        room_no=room,
        category=category,
        description=description,
        status=status,
    )
    if status == "resolved":
        complaint.resolved_on = datetime.now()
    session.add(complaint)
    session.flush()

    if status == "in_progress" or status == "resolved":
        session.add(Updates(complaint_id=complaint.id, status="in_progress", note="Work has started"))
    if status == "resolved":
        session.add(Updates(complaint_id=complaint.id, status="resolved", note="Issue fixed"))

session.commit()
session.close()
print("8 complaints")