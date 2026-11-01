# Found & Returned

Found & Returned is the React interface for the Lost & Found item board. The Vite development server proxies `/items` requests to the API on `http://127.0.0.1:8000`.

## Run locally

Start either the Node API (`npm start` in `backend`) or the Python API (`python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000` in `backend`), then run:

```powershell
npm install
npm run dev
```

Open the Vite URL printed in the terminal, usually `http://localhost:5173`.
