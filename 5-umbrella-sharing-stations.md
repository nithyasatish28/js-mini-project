# PRD & Design Doc: Umbrella-Sharing Stations

Build an app for umbrella stations around campus, where students borrow an umbrella at one station and return it at any other: a **FastAPI + SQLite** backend and a **React** frontend. **Team: 2 students. Time: 2 days, with the demo on day 3.**

## 1. What to build

- Students borrow an umbrella from a station with their **roll number**, and return it at any station.
- Each station has a fixed number of slots, so a full station can't take more umbrellas.
- The campus staff add stations and see which ones are empty or full. There are no logins.

## 2. Data

One SQLite file, `umbrellas.db`, with two tables.

| Table | Columns |
| --- | --- |
| `stations` | `id`, `name`, `location`, `capacity`, `umbrellas_available` |
| `borrows` | `id`, `roll_no`, `from_station_id`, `to_station_id` (empty until returned), `borrowed_on`, `returned_on` (empty until returned) |

Free slots at a station = `capacity` − `umbrellas_available`.

Add **5 stations** to start with. Make at least one of them empty (0 umbrellas) and one full (no free slots).

## 3. API: 7 endpoints

Run it on port **8001**, and add CORS so the React app can call it.

**Before you write any code, fill in the empty columns.** Pick the method (GET, POST, PATCH or DELETE), the path, what the client sends, and the status codes. Use the rules in section 4 for the error codes.

| # | What it does | Method | Path | Request body | Success code | Error codes |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | Get all the stations. Each one includes its umbrellas available and its free slots. | | | | | |
| E2 | Get one station by its id. | | | | | |
| E3 | Add a new station: name, location, capacity, and how many umbrellas it starts with. | | | | | |
| E4 | Borrow an umbrella from a station with a roll number. The borrow date is today. | | | | | |
| E5 | Return an umbrella to a station (it can be a different station). The return date is today. | | | | | |
| E6 | Get one student's umbrella that isn't returned yet, by roll number. It includes the name of the station it came from. | | | | | |
| E7 | Get the stations that need attention: empty ones (0 umbrellas) and full ones (0 free slots). | | | | | |

## 4. Rules the API must check

| Rule | Status |
| --- | --- |
| Borrowing from a station with 0 umbrellas | 409 |
| Borrowing when the student already has an umbrella not returned | 409 |
| Returning to a station that is full | 409 |
| Returning an umbrella that was already returned | 409 |
| A station or borrow id that doesn't exist | 404 |
| A missing or empty field, `capacity` not between 1 and 30, or starting umbrellas not between 0 and `capacity` | 422 |

Borrowing takes 1 from the station's `umbrellas_available`. Returning adds 1 to the station it is returned to, which may be a different one. Every error sends a clear message: `{"detail": "This station is full. Try another one."}`.

Hint: to make the station names show up in E6, join the two tables: `SELECT ... FROM borrows JOIN stations ON stations.id = borrows.from_station_id`.

## 5. Frontend

One page with three parts. Keep the API address in one place: `const API_URL = "http://127.0.0.1:8001";`

| Part | Shows | Does | Uses |
| --- | --- | --- | --- |
| Stations | a card per station: name, location, umbrellas available, free slots, and an "Empty" or "Full" label; click one to see its details | a **Needs attention** button; roll number box + **Borrow** | E1, E2, E4, E7 |
| My umbrella | the student's umbrella not yet returned, and where it came from | type roll number + **Show**; pick a station from a dropdown + **Return** | E5, E6 |
| Add a station | a form | adds a station to the list | E3 |

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
- [ ] Borrowing at one station and returning at another changes both stations' counts without a refresh.
- [ ] The API's error messages show on the page.
- [ ] The data is still there after restarting the API.

## 8. Submit and marks

One GitHub repo with `backend/`, `frontend/` (without `node_modules`) and a `README.md` that says how to run both. Both partners must be able to explain any part of the code.

| Part | Marks |
| --- | --- |
| Endpoints and rules | 40 |
| Frontend connected to the API | 40 |
| README and demo (explain your code) | 20 |

**Bonus, if you finish early:** a list of the student's past borrows, the most-used station, or `pytest` tests for the rules.
