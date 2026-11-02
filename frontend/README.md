# Hostel Care

Hostel Care is the React interface for raising, viewing, and managing hostel complaints. The Vite development server proxies `/complaints` requests to the API on `http://127.0.0.1:8000`.

## Run locally

Open two terminals from the project root.

**Terminal 1 — API:** Start either the Node API or the Python API. Keep this terminal running.

```powershell
cd backend
npm start
```

Alternatively, run the FastAPI implementation from `backend` with `python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000`.

**Terminal 2 — frontend:**

```powershell
cd frontend
npm install
npm run dev
```

Open the Vite URL printed in the terminal, usually `http://localhost:5173`.
