# Team 19 · Adopt-a-Plant

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 19 | Harsita | Hemanth Singh | [Adopt-a-Plant](https://github.com/nithyasatish28/js-mini-project/blob/main/4-adopt-a-plant.md) | `team-19-plants` |

**Every 3 hours:** update this file, then commit and push it with the message `Check-in Day 1 12:00` (your day and time). Your instructor reads this page on GitHub.

## 1. Who is doing what

Update your own row at every check-in.

| Day | Partner | What will you do? | Completed? | What are you going to work on next? | Stuck on? |
|---|---|---|---|---|---|
| Day 1 | Harsita |Create a Database, | Yes | E2, E4, E6  | No |
| Day 1 | Hemanth Singh | E1,  |  yes | E3, E5, E7 | WAS STUCKED BUT FIXED THE PROBLEM |
| Day 2 | Harsita | E2, E4, E6  | Yes | Frontend | YES, SOME CHANGES STILL PENDING|
| Day 2 | Hemanth Singh | E3, E5, E7 |yes | FRONTEND | No |
| Day 3 | Harsita | Frontend | KIND OF | PRESENTATION | IN PARTS  |
| Day 3 | Hemanth Singh |  |  |  |  |

## 2. Endpoint tracker

Fill in the method and path from your PRD's endpoint table. Status: ✅ done · 🟡 in progress · ⬜ not started

| # | Method + path | Built | Rules checked in /docs | Connected to React | Who |
|---|---|---|---|---|---|
| E1 | Get/Plants  |✅| ✅ | ✅| ✅ |Hemant|
| E2 | get/plants/{id} | ✅ | ✅| ✅ |Harsita|
| E3 | Post/plants | ✅ | ✅| ✅ |Hemant|
| E4 | patch/plants/{id}/adopt | ✅ | ✅| ✅|Harsita|
| E5 | patch/plants/{id}/unadopt | ✅ |✅| ✅ |Hemant|
| E6 | post/plants/{id}/water | ✅ | ✅| ✅ |Harsita|
| E7 | Get/plants/need-water | ✅ | ✅| ✅ |Hemant|
s
## 3. Frontend tracker

| Part (from section 5 of your PRD) | Shows the data | Buttons work | Shows API errors | Who |
|---|---|---|---|---|
| Garden | ✅ | ✅| ✅ | BOTH |
| My plants | ✅ | ✅| ✅ | BOTH |
| Add a plant |✅ | ✅| ✅| BOTH |

## 4. Blockers and help needed
I faced a merge error in VS Code that took about 1 hour. i tried doing everything but still  could'nt solve it but finally i used AI and, finally solved the problem.
- 

## 5. How to run our app

Fill this in by the end of Day 2. Someone who has never seen your code should be able to follow it.

**Backend**

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload

```

**Frontend**

```bash
cd frontend
npm install
npm run dev


```

## 6. Proof of work

Save a screenshot of `/docs` or your app as `screenshot.png` in this branch. It shows here:

![Our app](screenshot.png)
