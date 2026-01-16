# mP - backend + frontend

This workspace contains:
- a Flask backend at the repository root that exposes `/fake-users` and `/data` endpoints
- a Vite + React frontend in the `mP` subfolder that fetches data from the Flask API

Quick start

1. Create and activate a Python virtualenv in the project root and install backend deps:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the Flask backend (defaults to port 5000):

```bash
python3 app.py
```

3. In a separate terminal, start the frontend (the `mP` folder contains a Vite app):

```bash
cd mP
npm install
npm run dev
```

4. Open the Vite dev server address (typically `http://localhost:5173`) and the React app will fetch from `http://127.0.0.1:5000/fake-users`.

Notes
- CORS is enabled on the Flask side so requests from the React dev server should work.
- The backend stores generated users in memory; if you want persistence, ask and I can add file/DB storage.
