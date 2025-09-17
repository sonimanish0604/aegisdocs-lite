from pydantic import BaseModel

class AnalyzeResult(BaseModel):
    encrypted: bool
    embedded_files: bool
    embedded_javascript: bool
    fake_pdf: bool
    details: dict