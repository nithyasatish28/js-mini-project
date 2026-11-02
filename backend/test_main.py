import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_e1_get_all_events():
    response = client.get("/events")
    assert response.status_code == 200
    events = response.json()
    assert isinstance(events, list)
    assert len(events) >= 8


def test_e1_get_events_filtered_by_category():
    response = client.get("/events?category=sports")
    assert response.status_code == 200
    events = response.json()
    for ev in events:
        assert ev["category"] == "sports"


def test_e2_get_one_event():
    # Get all events to find a valid ID
    events = client.get("/events").json()
    valid_id = events[0]["id"]

    response = client.get(f"/events/{valid_id}")
    assert response.status_code == 200
    assert response.json()["id"] == valid_id


def test_e2_get_nonexistent_event():
    response = client.get("/events/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


def test_e3_add_event_valid():
    payload = {
        "title": "Robotics Expo",
        "club": "Robotics Club",
        "category": "technical",
        "event_date": "2026-12-15",
        "total_seats": 50
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Event added successfully"
    assert "event_id" in data


def test_e3_add_event_invalid_category_422():
    payload = {
        "title": "Invalid Event",
        "club": "Club",
        "category": "not-a-category",
        "event_date": "2026-12-15",
        "total_seats": 50
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 422


def test_e3_add_event_invalid_seats_422():
    payload = {
        "title": "Invalid Seats",
        "club": "Club",
        "category": "workshop",
        "event_date": "2026-12-15",
        "total_seats": 300  # greater than 200
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 422


def test_e3_add_event_invalid_date_422():
    payload = {
        "title": "Invalid Date",
        "club": "Club",
        "category": "seminar",
        "event_date": "15-12-2026",  # not YYYY-MM-DD
        "total_seats": 50
    }
    response = client.post("/events", json=payload)
    assert response.status_code == 422


def test_e4_and_e5_registration_and_delete_rules():
    # Create a fresh event for testing
    event_res = client.post("/events", json={
        "title": "Hackathon 2026",
        "club": "Dev Club",
        "category": "technical",
        "event_date": "2026-12-20",
        "total_seats": 2
    })
    event_id = event_res.json()["event_id"]

    # Register student 1
    reg_res1 = client.post(f"/events/{event_id}/registrations", json={"roll_no": "CS101"})
    assert reg_res1.status_code == 201
    reg1_id = reg_res1.json()["registration_id"]

    # Check seats left decremented to 1
    ev_check = client.get(f"/events/{event_id}").json()
    assert ev_check["seats_left"] == 1

    # Rule: Registering for the same event twice -> 409
    dup_res = client.post(f"/events/{event_id}/registrations", json={"roll_no": "CS101"})
    assert dup_res.status_code == 409
    assert dup_res.json()["detail"] == "Already registered for this event."

    # Rule: Deleting an event with active registrations -> 409
    del_res = client.delete(f"/events/{event_id}")
    assert del_res.status_code == 409
    assert del_res.json()["detail"] == "Cannot delete event with active registrations"

    # Register student 2 (filling the event, 0 seats left)
    reg_res2 = client.post(f"/events/{event_id}/registrations", json={"roll_no": "CS102"})
    assert reg_res2.status_code == 201
    reg2_id = reg_res2.json()["registration_id"]

    # Rule: Registering for an event with 0 seats left -> 409
    full_res = client.post(f"/events/{event_id}/registrations", json={"roll_no": "CS103"})
    assert full_res.status_code == 409
    assert full_res.json()["detail"] == "This event is full."

    # E6: Get student registrations
    st_regs = client.get("/registrations/CS101").json()
    assert any(r["registration_id"] == reg1_id for r in st_regs)

    # E7: Cancel registration
    cancel_res1 = client.patch(f"/registrations/{reg1_id}/cancel")
    assert cancel_res1.status_code == 200

    # Rule: Cancelling a registration that was already cancelled -> 409
    dup_cancel = client.patch(f"/registrations/{reg1_id}/cancel")
    assert dup_cancel.status_code == 409
    assert dup_cancel.json()["detail"] == "Registration already cancelled."

    # Cancelling reg1 increased seats back to 1
    ev_check2 = client.get(f"/events/{event_id}").json()
    assert ev_check2["seats_left"] == 1

    # Cancel reg2 as well
    client.patch(f"/registrations/{reg2_id}/cancel")

    # Now that no active registrations remain, deleting event should succeed
    del_ok = client.delete(f"/events/{event_id}")
    assert del_ok.status_code == 200

    # Now event is gone -> 404
    assert client.get(f"/events/{event_id}").status_code == 404


def test_rule_past_event_registration_409():
    # Find the past event seeded in database (Python Introduction, 2026-10-01)
    events = client.get("/events").json()
    past_event = next((e for e in events if e["event_date"] < "2026-11-02"), None)
    if past_event:
        res = client.post(f"/events/{past_event['id']}/registrations", json={"roll_no": "TEST_ROLL"})
        assert res.status_code == 409
        assert res.json()["detail"] == "Event has already passed."
