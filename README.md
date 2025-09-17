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

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload