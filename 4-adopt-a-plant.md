# PRD & Design Doc: Adopt-a-Plant

Build an app that lets students adopt the plants around campus and look after them: a **FastAPI + SQLite** backend and a **React** frontend. **Team: 2 students. Time: 2 days, with the demo on day 3.**

## 1. What to build

- The garden team adds the campus plants, each with how often it needs water.
- A student adopts a plant with their **roll number**, waters it, and logs each watering.
- Anyone can see which plants need water today. There are no logins.

## 2. Data

One SQLite file, `garden.db`, with two tables.

| Table | Columns |
| --- | --- |
| `plants` | `id`, `name`, `type`, `location`, `water_every_days`, `adopted_by` (empty if nobody has adopted it) |
| `waterings` | `id`, `plant_id`, `roll_no`, `watered_on` |

`type` must be one of: `succulent`, `flowering`, `herb`, `indoor`, `tree`.

Add **10 plants** to start with. Leave some not adopted, and add a few waterings so that at least one plant is due for water today.

A plant **needs water** when it has never been watered, or when its last watering was `water_every_days` or more days ago.

## 3. API: 7 endpoints

Run it on port **8001**, and add CORS so the React app can call it.

**Before you write any code, fill in the empty columns.** Pick the method (GET, POST, PATCH or DELETE), the path, what the client sends, and the status codes. Use the rules in section 4 for the error codes.

| # | What it does | Method | Path        | Request body                                      | Success code | Error codes     |
| --- | --- |--------|-------------|---------------------------------------------------|--------------|-----------------|
| E1 | Get all the plants. Can be filtered by type. Each one includes its last watered date. | GET    | /plants?type={type} | NA                                                | 200          |     404       |
| E2 | Get one plant by its id, with its list of waterings, newest first. | GET    | /plants/{plant_id} | NA                                                | 200          | 404             |
| E3 | Add a new plant: name, type, location and how often it needs water. Nobody has adopted it yet. | POST   | /plants     | {name:"",type="",location="",water_every_days=""} | 201          | 422,400         |
| E4 | Adopt a plant with a roll number. | PATCH  | /plants/{plant_id} | {adopted_by:""}                                   | 200          | 404 , 409       |
| E5 | Give up (un-adopt) a plant. | PATCH  | /plant/{plant_id} | {adopted_by:null}                                 | 200          | 404,409         |
| E6 | Log a watering with a roll number. The watering date is today. | POST   | /water      | {plant_id:"",roll_no:""}                            | 201          | 403,404,409,422 |
| E7 | Get the plants that need water today. |        |             |                                                   |              |                 |

## 4. Rules the API must check

| Rule | Status |
| --- | --- |
| Adopting a plant that someone else has already adopted | 409 |
| Adopting when the student already has 2 plants | 409 |
| Giving up a plant that nobody has adopted | 409 |
| Watering a plant you haven't adopted | 403 |
| Watering the same plant twice on the same day | 409 |
| A plant id that doesn't exist | 404 |
| A missing or empty field, a type not in the list, or `water_every_days` not between 1 and 14 | 422 |

Every error sends a clear message: `{"detail": "Only the student who adopted this plant can water it."}`. 403 means "you're not allowed to do this".

Hint for dates: `from datetime import date`, then `(date.today() - date.fromisoformat(last_watered)).days` gives the number of days since the last watering.

## 5. Frontend

One page with three parts. Keep the API address in one place: `const API_URL = "http://127.0.0.1:8001";`

| Part | Shows | Does | Uses |
| --- | --- | --- | --- |
| Garden | a card per plant: name, type, location, who adopted it, last watered, and a "Needs water" label | type filter; a **Needs water today** button; roll number box + **Adopt** | E1, E4, E7 |
| My plants | the student's plants; click one to see its waterings | type roll number + **Show**; **Water** and **Give up** buttons | E2, E5, E6 |
| Add a plant | a form with a type dropdown | adds a plant to the garden | E3 |

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
- [ ] Watering a plant updates its last watered date and removes its "Needs water" label, without a refresh.
- [ ] Watering someone else's plant shows the API's message on the page.
- [ ] The data is still there after restarting the API.

## 8. Submit and marks

One GitHub repo with `backend/`, `frontend/` (without `node_modules`) and a `README.md` that says how to run both. Both partners must be able to explain any part of the code.

| Part | Marks |
| --- | --- |
| Endpoints and rules | 40 |
| Frontend connected to the API | 40 |
| README and demo (explain your code) | 20 |

**Bonus, if you finish early:** a leaderboard of who has watered the most, a "days until next watering" count on each card, or `pytest` tests for the rules.
