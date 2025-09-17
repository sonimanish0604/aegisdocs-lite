# PDF Analyzer (Lite)

A **feedback-first** FastAPI service that flags risky traits in PDFs:
- Encrypted
- Embedded files
- Embedded JavaScript
- Fake/invalid PDF header (heuristic)

> 🧪 This is a **lite** version intended for community testing & feedback.
> The production API includes API keys, rate limiting, usage logs, and
> deployment hardening — those are **not** included here.

## Quickstart

# 1) create & activate venv
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate

# 2) install deps
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 3) run (more reliable on Windows PATH)
python -m uvicorn app.main:app --reload
# App: http://127.0.0.1:8000  |  Docs: http://127.0.0.1:8000/docs
