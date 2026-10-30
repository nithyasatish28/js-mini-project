# PRD & Design Doc: Hostel Complaint Tracker

Build a complaint tracker for the campus hostel: a **FastAPI + SQLite** backend and a **React** frontend. **Team: 2 students. Time: 2 days, with the demo on day 3.**

## 1. What to build

- Students raise a complaint about their room (for example, a broken fan) with their **roll number**, and follow its progress.
- The warden moves each complaint forward as the work gets done: **open → in progress → resolved**.
- There are no logins.

## 2. Data

One SQLite file, `hostel.db`, with two tables.

| Table | Columns |
| --- | --- |
| `complaints` | `id`, `roll_no`, `room_no`, `category`, `description`, `status`, `created_on`, `resolved_on` (empty until resolved) |
| `updates` | `id`, `complaint_id`, `status`, `note`, `updated_on` |

`category` must be one of: `electrical`, `plumbing`, `furniture`, `cleaning`, `internet`.
`status` is one of: `open`, `in_progress`, `resolved`.

Add **8 complaints** to start with, with all three statuses.

## 3. API: 7 endpoints

Run it on port **8001**, and add CORS so the React app can call it.

**Before you write any code, fill in the empty columns.** Pick the method (GET, POST, PATCH or DELETE), the path, what the client sends, and the status codes. Use the rules in section 4 for the error codes.

| # | What it does | Method | Path | Request body | Success code | Error codes |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | Get all the complaints. Can be filtered by status and by category. | | | | | |
| E2 | Get one complaint by its id, with its list of updates. | | | | | |
| E3 | Raise a complaint: roll number, room number, category and description. It starts as `open`. | | | | | |
| E4 | Move a complaint to its next status, with a note. This also adds a row to `updates`. | | | | | |
| E5 | Get one student's complaints, by roll number. | | | | | |
| E6 | Delete a complaint. | | | | | |
| E7 | Get how many complaints there are in each status, e.g. `{"open": 3, "in_progress": 2, "resolved": 5}`. | | | | | |

## 4. Rules the API must check

| Rule | Status |
| --- | --- |
| Skipping a status (open straight to resolved), or going backwards | 409 |
| Changing a complaint that is already resolved | 409 |
| Deleting a complaint that is not `open` any more | 409 |
| Raising a complaint when the same room already has an unresolved complaint in that category | 409 |
| A complaint id that doesn't exist | 404 |
| A missing or empty field, a category not in the list, or a description shorter than 10 characters | 422 |

When a complaint becomes `resolved`, set `resolved_on` to today. Every error sends a clear message: `{"detail": "A complaint can only move one step at a time."}`.

Hint for the status order: keep the next step in a dictionary, `{"open": "in_progress", "in_progress": "resolved"}`.

## 5. Frontend

One page with three parts. Keep the API address in one place: `const API_URL = "http://127.0.0.1:8001";`

| Part | Shows | Does | Uses |
| --- | --- | --- | --- |
| Warden | the counts per status at the top; a card per complaint with a coloured status label | status and category filters; a note box + **Move to next status** button | E1, E4, E7 |
| My complaints | the student's complaints; click one to see its updates | type roll number + **Show**; **Delete** button on open complaints | E2, E5, E6 |
| Raise a complaint | a form with a category dropdown | adds a complaint | E3 |

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
- [ ] Moving a complaint forward updates its label and the counts without a refresh.
- [ ] The API's error messages show on the page.
- [ ] The data is still there after restarting the API.

## 8. Submit and marks

One GitHub repo with `backend/`, `frontend/` (without `node_modules`) and a `README.md` that says how to run both. Both partners must be able to explain any part of the code.

| Part | Marks |
| --- | --- |
| Endpoints and rules | 40 |
| Frontend connected to the API | 40 |
| README and demo (explain your code) | 20 |

**Bonus, if you finish early:** show how many days each complaint has been open, sort by oldest first, or `pytest` tests for the rules.
