# Backend & Frontend Deployment

This document explains how to run the backend (FastAPI) and frontend (Next.js) locally and how to configure the frontend to call the backend via an environment variable.

1. Backend (development)

- Create and activate your Python environment and install dependencies:

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1   # PowerShell
pip install -r backend/requirements.txt
```

- Run the FastAPI server (local dev):

```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

This exposes the predict endpoint at `http://127.0.0.1:8000/predict`.

2. Frontend (development)

- Install frontend dependencies and run the dev server from the repository root (or `frontend` folder):

```bash
cd frontend
npm install
npm run dev
```

- Configure the backend URL for the frontend by creating a `.env.local` file in the `frontend` folder with the following value:

```
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

The Next.js client-side code uses `process.env.NEXT_PUBLIC_API_URL` to construct requests. If the variable is not set the frontend falls back to `http://127.0.0.1:8000`.

3. Production notes

- In production, set `NEXT_PUBLIC_API_URL` to the production backend URL (for example, `https://api.example.com`). Provide this env var at build-time or via your hosting platform's environment configuration.
- Build the frontend with `npm run build` then `npm run start` (or use your hosting provider). Ensure CORS is properly configured on the backend for your frontend origin.

4. Additional recommendations

- Persist trained model artifacts to a writable path accessible by the backend; `backend/app/models/model.joblib` is used by default in development.
- Use HTTPS for production backend endpoints.
- Add health and metrics endpoints on the backend for easier monitoring.
