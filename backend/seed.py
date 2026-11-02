import functions
complaints = [
    {"roll_no": "401", "room_no": "101", "category": "electrical", "description": "Ceiling fan is not working", "notes": []},
    {"roll_no": "402", "room_no": "102", "category": "plumbing", "description": "Tap in the bathroom is leaking", "notes": []},
    {"roll_no": "403", "room_no": "103", "category": "internet", "description": "Wifi keeps disconnecting every hour", "notes": []},
    {"roll_no": "404", "room_no": "104", "category": "furniture", "description": "Study table drawer is broken", "notes": ["Carpenter will visit tomorrow"]},
    {"roll_no": "405", "room_no": "105", "category": "cleaning", "description": "Room has not been cleaned this week", "notes": ["Cleaning staff informed"]},
    {"roll_no": "406", "room_no": "106", "category": "electrical", "description": "Tube light flickers all night", "notes": ["Electrician assigned"]},
    {"roll_no": "407", "room_no": "107", "category": "plumbing", "description": "Water heater is not heating", "notes": ["Plumber assigned", "Heater replaced"]},
    {"roll_no": "408", "room_no": "108", "category": "internet", "description": "No signal on the room router", "notes": ["Router checked", "New router installed"]},
]

if functions.get_all_complaints() == []:
    for complaint in complaints:
        added = functions.add_new_complaint(
            roll_no=complaint["roll_no"],
            room_no=complaint["room_no"],
            category=complaint["category"],
            description=complaint["description"],
        )
        # each note moves the complaint one step forward and adds a row to Updates
        for note in complaint["notes"]:
            functions.update_complaint(complaint_id=added["id"], note=note)