import os, tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import AnalyzeResult
from app.analyzer import analyze_pdf

MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))  # demo cap
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")  # e.g., "*" or "https://your.site"

app = FastAPI(
    title="PDF Analyzer (Lite Demo)",
    version="0.1.1",
    description="Public demo for community feedback. Files are processed in-memory and not persisted."
)

# CORS: for demo, * is fine; lock down later if embedding in your site
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "env": "demo"}

@app.get("/beta-info")
def beta_info():
    return {
        "name": "PDF Analyzer (Lite Demo)",
        "version": "0.1.1",
        "max_upload_mb": MAX_UPLOAD_MB,
        "notes": "Do not upload sensitive or malicious content. Feedback welcome!",
        "feedback": "Add your Google Form or GitHub Issues URL here"
    }

@app.post("/analyze", response_model=AnalyzeResult)
async def analyze(file: UploadFile = File(...)):
    # Basic content-type guard (best-effort; clients sometimes send generic types)
    if not (file.content_type in {"application/pdf", "application/x-pdf", "binary/octet-stream"}):
        # allow generic binary too; we hard-check the header below
        pass

    # Read with size cap
    data = await file.read()
    size_mb = len(data) / (1024 * 1024)
    if size_mb > MAX_UPLOAD_MB:
        raise HTTPException(status_code=413, detail=f"File too large. Max {MAX_UPLOAD_MB} MB.")

    # Quick PDF header sniff
    if len(data) < 5 or not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="Not a valid PDF (missing %PDF- header).")

    # Save to temp, analyze, delete
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(data)
        tmp_path = tmp.name

    try:
        result = analyze_pdf(tmp_path)
        return AnalyzeResult(**result)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
