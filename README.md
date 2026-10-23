# MPLADS Sentinel
Secure MVP for monitoring **synthetic** development works. Deterministic rules flag records for human review; the optional Gemini adapter explains findings but never changes scores. No allegations of corruption or fraud are made.

## Local setup (Windows / VS Code)
Backend: `cd backend`; `py -3.12 -m venv .venv`; activate `.venv`; `pip install -r requirements.txt`; copy `.env.example` to `.env`; `python scripts/seed_data.py`; `uvicorn app.main:app --reload`.
Frontend: `cd frontend`; `npm install`; copy `.env.example` to `.env`; `npm run dev`.
API docs: http://localhost:8000/docs. Docker: `docker compose up --build`.

Local mode uses `AUTH_MODE=mock` and `X-Demo-Role` headers; never deploy mock auth. Production uses Firebase ID tokens/custom claims. See `docs/architecture.md`, `SECURITY.md`, `EVALUATION.md`.
Synthetic fixtures: 240 works, 20 evidence records, and invalid-row examples in `data/`.
