# Team 08 · Lab Equipment Booking

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 08 | H A Bhuvan | Pavan Kumar | [Lab Equipment Booking](https://github.com/nithyasatish28/js-mini-project/blob/main/3-lab-equipment-booking.md) | `team-08-lab` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | H A Bhuvan | README.md & Frontend Part,App.jsx and Bookeqip.jsx |  |  |  |
| Day 1 | Pavan Kumar | README & In backend part, presently creating database  |  |  |  |
| Day 2 | H A Bhuvan |  |  |  |  |
| Day 2 | Pavan Kumar |  |  |  |  |
| Day 3 | H A Bhuvan |  |  |  |  |
| Day 3 | Pavan Kumar |  |  |  |  |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 |  | ⬜ | ⬜ | ⬜ |  |
| E2 |  | ⬜ | ⬜ | ⬜ |  |
| E3 |  | ⬜ | ⬜ | ⬜ |  |
| E4 |  | ⬜ | ⬜ | ⬜ |  |
| E5 |  | ⬜ | ⬜ | ⬜ |  |
| E6 |  | ⬜ | ⬜ | ⬜ |  |
| E7 |  | ⬜ | ⬜ | ⬜ |  |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Equipment | ⬜ | ⬜ | ⬜ |  |
| My bookings | ⬜ | ⬜ | ⬜ |  |
| Add equipment | ⬜ | ⬜ | ⬜ |  |

## 4. Blockers and help needed

- 

## 5. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.

**Backend**

```bash
cd backend

```

**Frontend**

```bash
cd frontend

```

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)



# PRD & Design Doc: Lab Equipment Booking

Build a booking app for the department's lab equipment: a **FastAPI + SQLite** backend and a **React** frontend. **Team: 2 students. Time: 2 days, with the demo on day 3.**

## 1. What to build

- Students see the lab's equipment, book an item for a day with their **roll number**, and cancel the booking.
- The lab assistant adds equipment and marks items out of service when they break.
- There are no logins.

## 2. Data

One SQLite file, `lab.db`, with two tables.

| Table | Columns |
| --- | --- |
| `equipment` | `id`, `name`, `type`, `lab_room`, `in_service` (1 or 0) |
| `bookings` | `id`, `equipment_id`, `roll_no`, `booking_date`, `booked_on`, `cancelled` (0 or 1) |

`type` must be one of: `microscope`, `oscilloscope`, `3d-printer`, `laptop`, `camera`.

Add **10 items** to start with, and mark at least one of them out of service.

## 3. API: 7 endpoints

Run it on port **8001**, and add CORS so the React app can call it.

**Before you write any code, fill in the empty columns.** Pick the method (GET, POST, PATCH or DELETE), the path, what the client sends, and the status codes. Use the rules in section 4 for the error codes.

| # | What it does | Method | Path | Request body | Success code | Error codes |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | Get all the equipment. Can be filtered by type. |GET  | | | | |
| E2 | Get one item by its id. |GET | | | | |
| E3 | Add a new item: name, type and lab room. It starts in service. |POST| | | | |
| E4 | Mark an item in service or out of service. |PATCH | | | | |
| E5 | Book an item for a date with a roll number. The booked-on date is today. |POST | | | | |
| E6 | Get one student's bookings that aren't cancelled and are today or later, by roll number. Each one includes the item's name. |GET| | | | |
| E7 | Cancel a booking. |POST||||||

## 4. Rules the API must check

| Rule | Status |
| --- | --- |
| Booking an item that is out of service | 409 |
| Booking an item that is already booked (and not cancelled) for that date | 409 |
| Booking when the student already has 2 bookings for that date | 409 |
| Cancelling a booking that was already cancelled | 409 |
| An item or booking id that doesn't exist | 404 |
| A missing or empty field, a type not in the list, or a date not written as `YYYY-MM-DD` | 422 |
| A booking date in the past, or more than 7 days from today | 422 |

Cancelling a booking frees that date, so someone else can book the item. Every error sends a clear message: `{"detail": "This item is already booked for that day."}`.

Hint for dates: `from datetime import date, timedelta`, then compare `date.fromisoformat(booking_date)` with `date.today()` and `date.today() + timedelta(days=7)`.

## 5. Frontend

One page with three parts. Keep the API address in one place: `const API_URL = "http://127.0.0.1:8001";`

| Part | Shows | Does | Uses |
| --- | --- | --- | --- |
| Equipment | a card per item: name, type, room, and an "Out of service" label | type filter; date picker + roll number box + **Book**; **In / Out of service** button | E1, E4, E5 |
| My bookings | the student's bookings with dates | type roll number + **Show**; **Cancel** button | E6, E7 |
| Add equipment | a form with a type dropdown | adds an item to the list | E3 |

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
- [ ] Booking the same item twice for the same date shows the API's message, and cancelling frees the date.
- [ ] Marking an item out of service updates its card without a refresh.
- [ ] The data is still there after restarting the API.

## 8. Submit and marks

One GitHub repo with `backend/`, `frontend/` (without `node_modules`) and a `README.md` that says how to run both. Both partners must be able to explain any part of the code.

| Part | Marks |
| --- | --- |
| Endpoints and rules | 40 |
| Frontend connected to the API | 40 |
| README and demo (explain your code) | 20 |

**Bonus, if you finish early:** show which dates an item is already booked, a search box, or `pytest` tests for the rules.

