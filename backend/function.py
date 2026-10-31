
import sqlite3
from pathlib import Path
from datetime import date


DB_PATH = Path(__file__).parent / "events.db"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn




def get_events(category=None):
    conn = connect()

    if category:
        rows = conn.execute(
            "SELECT * FROM events WHERE category = ? ORDER BY id",
            (category.lower(),)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM events ORDER BY id"
        ).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def get_event(event_id):
    conn = connect()
    row = conn.execute(
        "SELECT * FROM events WHERE id = ?", (event_id,)
    ).fetchone()
    conn.close()

    return dict(row) if row else None


def add_event(data):
    conn = connect()

    with conn:
        event_id = conn.execute(
            """
            INSERT INTO events
            (title, club, category, event_date, total_seats, seats_left)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data["title"], data["club"], data["category"],
                data["event_date"], data["total_seats"],
                data["total_seats"]
            )
        ).lastrowid

    conn.close()
    return get_event(event_id)


def delete_event(event_id):
    conn = connect()

    event = conn.execute(
        "SELECT id FROM events WHERE id = ?", (event_id,)
    ).fetchone()

    if event is None:
        conn.close()
        return "not_found"

    count = conn.execute(
        """
        SELECT COUNT(*) FROM registrations
        WHERE event_id = ? AND cancelled_on IS NULL
        """,
        (event_id,)
    ).fetchone()[0]

    if count > 0:
        conn.close()
        return "registered"

    conn.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    return "deleted"




def register_student(event_id, roll_no):
    conn = connect()

    event = conn.execute(
        "SELECT * FROM events WHERE id = ?", (event_id,)
    ).fetchone()

    if event is None:
        conn.close()
        return "not_found"

    if event["event_date"] < date.today().isoformat():
        conn.close()
        return "past_event"

    if event["seats_left"] <= 0:
        conn.close()
        return "full"

    old = conn.execute(
        """
        SELECT id FROM registrations
        WHERE event_id = ? AND roll_no = ?
        AND cancelled_on IS NULL
        """,
        (event_id, roll_no)
    ).fetchone()

    if old:
        conn.close()
        return "already_registered"

    with conn:
        conn.execute(
            """
            INSERT INTO registrations
            (event_id, roll_no, registered_on)
            VALUES (?, ?, ?)
            """,
            (event_id, roll_no, date.today().isoformat())
        )

        conn.execute(
            """
            UPDATE events SET seats_left = seats_left - 1
            WHERE id = ?
            """,
            (event_id,)
        )

    conn.close()
    return "success"




def get_student_registrations(roll_no):
    conn = connect()

    rows = conn.execute(
        """
        SELECT registrations.id, registrations.roll_no,
               registrations.registered_on,
               events.title, events.event_date
        FROM registrations
        JOIN events ON events.id = registrations.event_id
        WHERE registrations.roll_no = ?
        AND registrations.cancelled_on IS NULL
        """,
        (roll_no,)
    ).fetchall()

    conn.close()
    return [dict(row) for row in rows]


def cancel_registration(registration_id):
    conn = connect()

    reg = conn.execute(
        "SELECT * FROM registrations WHERE id = ?",
        (registration_id,)
    ).fetchone()

    if reg is None:
        conn.close()
        return "not_found"

    if reg["cancelled_on"] is not None:
        conn.close()
        return "already_cancelled"

    with conn:
        conn.execute(
            """
            UPDATE registrations
            SET cancelled_on = ?
            WHERE id = ?
            """,
            (date.today().isoformat(), registration_id)
        )

        conn.execute(
            """
            UPDATE events SET seats_left = seats_left + 1
            WHERE id = ?
            """,
            (reg["event_id"],)
        )

    conn.close()
    return "success"
