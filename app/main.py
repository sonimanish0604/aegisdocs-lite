from fastapi import FastAPI, UploadFile, File
from app.models import AnalyzeResult
from app.analyzer import analyze_pdf
import tempfile, os

app = FastAPI(title="PDF Analyzer (Lite)", version="0.1.0")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalyzeResult)
async def analyze(file: UploadFile = File(...)):
    # Save to temp file (no persistence)
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        contents = await file.read()
        tmp.write(contents)
        tmp_path = tmp.name
    try:
        result = analyze_pdf(tmp_path)
        return AnalyzeResult(**result)
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass