from pypdf import PdfReader

def analyze_pdf(file_path: str) -> dict:
    # NOTE: lightweight, heuristic checks for demo/feedback
    details = {}
    try:
        reader = PdfReader(file_path)
        encrypted = reader.is_encrypted

        # Embedded files (very simplified: look for /EmbeddedFiles in catalog)
        embedded_files = False
        try:
            embedded_files = "/EmbeddedFiles" in (reader.trailer["/Root"].keys())
        except Exception:
            pass

        # JavaScript (very simplified: look for /JavaScript or /JS anywhere in trailer)
        def _has_js(obj) -> bool:
            try:
                s = str(obj)
                return "/JavaScript" in s or "/JS" in s
            except Exception:
                return False

        embedded_js = _has_js(reader.trailer)

        # Fake PDF (heuristic: header check)
        with open(file_path, "rb") as f:
            header = f.read(8)
        fake_pdf = not header.startswith(b"%PDF-")

        details.update({
            "num_pages": len(reader.pages) if not encrypted else None
        })

        return {
            "encrypted": bool(encrypted),
            "embedded_files": bool(embedded_files),
            "embedded_javascript": bool(embedded_js),
            "fake_pdf": bool(fake_pdf),
            "details": details
        }
    except Exception as e:
        # On parsing errors, treat as suspicious header
        return {
            "encrypted": False,
            "embedded_files": False,
            "embedded_javascript": False,
            "fake_pdf": True,
            "details": {"error": str(e)}
        }