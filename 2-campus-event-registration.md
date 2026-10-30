# PRD & Design Doc: Campus Event Registration

Build an event registration app for campus clubs: a **FastAPI + SQLite** backend and a **React** frontend. **Team: 2 students. Time: 2 days, with the demo on day 3.**

## 1. What to build

- Students see upcoming events, register with their **roll number**, and cancel if they can't go.
- Club coordinators add events and delete them.
- There are no logins.

## 2. Data

One SQLite file, `events.db`, with two tables.

| Table | Columns |
| --- | --- |
| `events` | `id`, `title`, `club`, `category`, `event_date`, `total_seats`, `seats_left` |
| `registrations` | `id`, `event_id`, `roll_no`, `registered_on`, `cancelled_on` (empty until cancelled) |

`category` must be one of: `technical`, `cultural`, `sports`, `workshop`, `seminar`.

Add **8 events** to start with. Give at least one of them 0 seats left, and give one an `event_date` that has already passed.

## 3. API: 7 endpoints

Run it on port **8001**, and add CORS so the React app can call it.

**Before you write any code, fill in the empty columns.** Pick the method (GET, POST, PATCH or DELETE), the path, what the client sends, and the status codes. Use the rules in section 4 for the error codes.

| # | What it does | Method | Path | Request body | Success code | Error codes |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | Get all the events. Can be filtered by category. | | | | | |
| E2 | Get one event by its id. | | | | | |
| E3 | Add a new event: title, club, category, date and total seats. Seats left start equal to total seats. | | | | | |
| E4 | Delete an event. | | | | | |
| E5 | Register for an event with a roll number. The registration date is today. | | | | | |
| E6 | Get one student's registrations that aren't cancelled, by roll number. Each one includes the event's title and date. | | | | | |
| E7 | Cancel a registration. The cancel date is today. | | | | | |

## 4. Rules the API must check

| Rule | Status |
| --- | --- |
| Registering for an event with 0 seats left | 409 |
| Registering for the same event twice (and not cancelled) | 409 |
| Registering for an event whose date has already passed | 409 |
| Cancelling a registration that was already cancelled | 409 |
| Deleting an event that still has registrations not cancelled | 409 |
| An event or registration id that doesn't exist | 404 |
| A missing or empty field, a category not in the list, `total_seats` not between 1 and 200, or a date not written as `YYYY-MM-DD` | 422 |

Registering takes 1 from `seats_left`, and cancelling adds 1 back. Every error sends a clear message: `{"detail": "This event is full."}`.

Hint for dates: `from datetime import date`, then `date.fromisoformat(event_date) < date.today()` is `True` for a past event.

## 5. Frontend

One page with three parts. Keep the API address in one place: `const API_URL = "http://127.0.0.1:8001";`

| Part | Shows | Does | Uses |
| --- | --- | --- | --- |
| Events | a card per event: title, club, date, seats left | category filter; roll number box + **Register**; **Delete** button | E1, E4, E5 |
| My events | the student's registrations with event dates | type roll number + **Show**; **Cancel** button | E6, E7 |
| Add an event | a form with a category dropdown and a date picker | adds an event to the list | E3 |

- Put each component in its own file in `src/components/`.
- After every action, the page updates without a refresh.
- When the API says no, show its `detail` message on the page.

## 6. Plan

| Day | Finish |
| --- | --- |
| Day 1 | Database + all 7 endpoints + the rules, tested in `/docs` |
| Day 2 | React app connected to the API |
| Day 3 | Demo |

Fill in the progress check-in every 3 hours.

## 7. Done when

- [ ] All 7 endpoints work in `/docs`.
- [ ] Each rule in section 4 gives the right status code.
- [ ] Register, then Cancel, changes the seats left on screen without a refresh.
- [ ] The API's error messages show on the page.
- [ ] The data is still there after restarting the API.

## 8. Submit and marks

One GitHub repo with `backend/`, `frontend/` (without `node_modules`) and a `README.md` that says how to run both. Both partners must be able to explain any part of the code.

| Part | Marks |
| --- | --- |
| Endpoints and rules | 40 |
| Frontend connected to the API | 40 |
| README and demo (explain your code) | 20 |

**Bonus, if you finish early:** a search box, a "Past" label on events that are over, or `pytest` tests for the rules.
