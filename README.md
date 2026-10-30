# JS Mini Project: FastAPI + React

Build a full-stack app in **pairs**: a **FastAPI + SQLite** backend and a **React** frontend.
**Time: 2 days, with the demo on day 3.**

## 1. The projects

Each pair builds **one** project. Open your project's file and read it fully before you start.

| # | Project | File | Teams |
|---|---|---|---|
| 1 | Hostel Complaint Tracker | [1-hostel-complaint-tracker.md](1-hostel-complaint-tracker.md) | 01, 06, 11, 16, 21 |
| 2 | Campus Event Registration | [2-campus-event-registration.md](2-campus-event-registration.md) | 02, 07, 12, 17, 22 |
| 3 | Lab Equipment Booking | [3-lab-equipment-booking.md](3-lab-equipment-booking.md) | 03, 08, 13, 18, 23 |
| 4 | Adopt-a-Plant | [4-adopt-a-plant.md](4-adopt-a-plant.md) | 04, 09, 14, 19, 24 |
| 5 | Umbrella-Sharing Stations | [5-umbrella-sharing-stations.md](5-umbrella-sharing-stations.md) | 05, 10, 15, 20, 25 |

**Before you write any code:** fill in the empty endpoint table (section 3 of your project file) and show it to your instructor.

## 2. Teams and branches

Find your team below. **Your branch name must match exactly:** small letters, no spaces.

| Team | Partner 1 | Partner 2 | Project | Branch |
|---|---|---|---|---|
| 01 | A Akshay | Lakshya R | 1 · Hostel Complaint Tracker | `team-01-hostel` |
| 02 | Adib Fareed Hasan | Tanush K | 2 · Campus Event Registration | `team-02-events` |
| 03 | Afifa Adeen | Syed Kaifuddin | 3 · Lab Equipment Booking | `team-03-lab` |
| 04 | Amruta Nagavi | Toshimah Devi Palanadoo | 4 · Adopt-a-Plant | `team-04-plants` |
| 05 | Ayushman Anand | Shafreen | 5 · Umbrella-Sharing Stations | `team-05-umbrellas` |
| 06 | Darsh Keshav | Rehaan Saha | 1 · Hostel Complaint Tracker | `team-06-hostel` |
| 07 | Gokul Reddy M | Abhishek Nayak | 2 · Campus Event Registration | `team-07-events` |
| 08 | H A Bhuvan | Pavan Kumar | 3 · Lab Equipment Booking | `team-08-lab` |
| 09 | Kommaddi Fayaz | Ganga Siva Kumar Reddy | 4 · Adopt-a-Plant | `team-09-plants` |
| 10 | Konduru Nanda Kishore Raju | Aditya Sivaji Perumalla | 5 · Umbrella-Sharing Stations | `team-10-umbrellas` |
| 11 | Melvin Jacob | Naman Choudhary | 1 · Hostel Complaint Tracker | `team-11-hostel` |
| 12 | Thanuja Reddy | Supriya R | 2 · Campus Event Registration | `team-12-events` |
| 13 | Monica Irala | Aryan Rao | 3 · Lab Equipment Booking | `team-13-lab` |
| 14 | Praneeth Reddy | Jashan S | 4 · Adopt-a-Plant | `team-14-plants` |
| 15 | Soham Nanduri | B Chaitanya | 5 · Umbrella-Sharing Stations | `team-15-umbrellas` |
| 16 | Samhita Bhuvanagiri | Aiman Patil | 1 · Hostel Complaint Tracker | `team-16-hostel` |
| 17 | Yashwant Gowda | S Mohammed Abrar ul Haq | 2 · Campus Event Registration | `team-17-events` |
| 18 | K. Jyoshna | Elluri Thammiksha | 3 · Lab Equipment Booking | `team-18-lab` |
| 19 | Harsita | Hemanth Singh | 4 · Adopt-a-Plant | `team-19-plants` |
| 20 | Sanghavi S | Naidile D | 5 · Umbrella-Sharing Stations | `team-20-umbrellas` |
| 21 | Jiken Pulinbhai Jasoliya | Vilok | 1 · Hostel Complaint Tracker | `team-21-hostel` |
| 22 | Shahiba Arshiya Banu | Madiha Shaik S | 2 · Campus Event Registration | `team-22-events` |
| 23 | Padmaraju Poojitha | S Thanmayee | 3 · Lab Equipment Booking | `team-23-lab` |
| 24 | Mohammed Shafi | Sarang Siva Thilakan | 4 · Adopt-a-Plant | `team-24-plants` |
| 25 | Sanika B Raj | Blessy Krupa S | 5 · Umbrella-Sharing Stations | `team-25-umbrellas` |

> **Never push to `main`.** Your pair works only on your own branch. Whatever is on your branch at the deadline is what gets marked.

## 3. Getting started with Git

The examples below use `team-01-hostel`. **Use your own branch name from the table.**

### Step 1 · Clone the repo (both partners)

```bash
git clone https://github.com/nithyasatish28/js-mini-project.git
cd js-mini-project
```

### Step 2 · Create your branch (Partner 1 only)

```bash
git switch -c team-01-hostel
git push -u origin team-01-hostel
```

### Step 3 · Get the branch (Partner 2 only)

```bash
git fetch
git switch team-01-hostel
```

Check that you're on the right branch: `git branch`. The line with `*` is the branch you're on.

### Step 4 · Save and push your work (every time something works)

```bash
git add .
git commit -m "Add E1 and E2"
git push
```

**Push at least every 3 hours**, before each progress check-in.

### Step 5 · Get your partner's work

```bash
git pull
```

Pull before you start working, and whenever your partner tells you they've pushed.

**Tip:** split the files. One partner works in `backend/`, the other in `frontend/`. Then you rarely edit the same file, and you avoid merge conflicts.

## 4. What your branch should look like

```
js-mini-project/
├── backend/        main.py, functions.py, your .db file, requirements.txt
├── frontend/       your Vite React app (without node_modules)
└── README.md       YOUR project's README (see below)
```

On your branch, **replace this README** with your own. It should have:

- your team number, both names, and the project name;
- how to run the backend and the frontend, step by step;
- your filled-in endpoint table.

These instructions stay on `main`, so you can always read them on GitHub.

## 5. Rules

1. **Never push to `main`**, and never push to another team's branch.
2. **Check your branch before you push:** `git branch`.
3. **Don't push big folders:** no `node_modules/` or `.venv/`. If `git add .` shows thousands of files, stop and ask.
4. **Write commit messages that say what changed:** "Add borrow rules", not "update".
5. **Fill in the progress check-in on Notion every 3 hours.**
6. **Both partners must be able to explain any part of the code.**

## 6. When Git says no

| Git says | Do this |
|---|---|
| `rejected … (fetch first)` | `git pull`, then `git push` |
| `nothing to commit, working tree clean` | Save your files in VS Code first |
| `src refspec … does not match any` | Commit before you push |
| You're on `main` (`git branch` shows `* main`) | `git switch` your branch name |
| `CONFLICT (content): Merge conflict in …` | Call your partner over, then ask your instructor |

## 7. Plan and submission

| Day | Finish |
|---|---|
| Day 1 | Database + all 7 endpoints + the rules, tested in `/docs` |
| Day 2 | React app connected to the API |
| Day 3 | Demo |

**Deadline:** [date and time]. The last commit pushed to your branch before the deadline is your submission.
