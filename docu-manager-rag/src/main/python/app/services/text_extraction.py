from fastapi import UploadFile
from typing import Union
import docx2txt
import csv
import json
from PyPDF2 import PdfReader

async def extract_text_from_file(file: UploadFile) -> str:
    content = await file.read()
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_pdf(content)
    elif filename.endswith(".docx"):
        return docx2txt.process(file.file)
    elif filename.endswith(".csv"):
        return extract_csv(content)
    elif filename.endswith(".json"):
        return extract_json(content)
    elif filename.endswith(".txt"):
        return content.decode("utf-8")
    else:
        raise ValueError("Unsupported file format")

def extract_pdf(content: bytes) -> str:
    from io import BytesIO
    reader = PdfReader(BytesIO(content))
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_csv(content: bytes) -> str:
    from io import StringIO
    rows = []
    f = StringIO(content.decode("utf-8"))
    reader = csv.reader(f)
    for row in reader:
        rows.append(" ".join(row))
    return "\n".join(rows)

def extract_json(content: bytes) -> str:
    data = json.loads(content)
    return json.dumps(data, indent=2)
