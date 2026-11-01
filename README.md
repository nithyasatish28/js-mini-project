# Team 20 · Umbrella-Sharing Stations

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 20 | Sanghavi S | Naidile D | [Umbrella-Sharing Stations](https://github.com/nithyasatish28/js-mini-project/blob/main/5-umbrella-sharing-stations.md) | `team-20-umbrellas` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Sanghavi S | Understand project requirements, design API endpoints and plan SQLite database structure. |started implementing API endpoints.|Complete backend functions and test all endpoints in Swagger.  | Understanding API parameters  |
<<<<<<< Updated upstream
<<<<<<< Updated upstream
| Day 1 | Naidile D | created a folder and cloned data switched to team 20 , understanding probem requirment. Imports from sqlalchemy , specifing path , created core interface that connects sqlite with python db(engine) , initializing the base class(base)  |  |  | terminal to run |
=======
| Day 1 | Naidile D | created a folder and cloned data switched to team 20 , understanding probem requirment  |Imports from sqlalchemy , specifing path , created core interface that connects sqlite with python db(engine) , initializing the base class(base)  |  |  |
>>>>>>> Stashed changes
=======
| Day 1 | Naidile D | created a folder and cloned data switched to team 20 , understanding probem requirment  |Imports from sqlalchemy , specifing path , created core interface that connects sqlite with python db(engine) , initializing the base class(base)  |  |  |
>>>>>>> Stashed changes
| Day 2 | Sanghavi S | Worked on backend database functions, implemented API endpoints for stations, borrowing and returning umbrellas, and added input validations. | Completed the main backend functions and API endpoints. | Test all endpoints and handle different error conditions in Swagger. | Connection errors|
| Day 2 | Naidile D | heavy spelling mistakes i faced captital and small letters also . insted of availability i was writing station in so  many places . / ? missing in some place . more space also error i faced . missing the arrow error . ? missing not found it shows . sometimes failed to fetch the data because of wrong terminal .  | i completed frontend statiolist , stationitem , addstation, myumbrella, app.jsx |  |  |
| Day 3 | Sanghavi S |Tested backend endpoints in Swagger  | Completed backend testing |  |  Debugging API responses and handling different validation cases.|
| Day 3 | Naidile D |  |  |  |  |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 |GET/stations  | ✅ | y⬜ | y⬜ |  |
| E2 |GET/stations/{station_id}  | ✅ | y⬜ | y⬜ |  |
| E3 |POST/stations  | ✅ | y⬜ | y⬜ |  |
| E4 |POST/borrow  | ✅ | y⬜ | y⬜ |  |
| E5 |PATCH /borrows/{borrow_id}/return  | ✅ | y⬜ | y⬜ |  |
| E6 |GET /students/{roll_no}/umbrella  | ✅ | y⬜ |y ⬜ |  |
| E7 |GET /stations/needs-attention | ✅ | y⬜ | y⬜ |  |

## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Stations | y⬜ | y⬜ | n⬜ |  |
| My umbrella | y⬜ | y⬜ | n⬜ |  |
| Add a station | y⬜ | y⬜ | n⬜ |  |

## 4. Blockers and help needed
To do some detailed work like creative thing .
- 

## 5. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.
open terminal in the project folder

**Backend**

```bash
cd backend
powershell terminal
python -m venv .venv
.venv\Scripts\activate
uvicorn main:app --port 8001

umbrellas.db creates automatically when swager runs 
```

**Frontend**

```bash
cd frontend
bash terminal
npm install
npm run dev

```

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
