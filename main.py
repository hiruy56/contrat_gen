from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from docx import Document
from fastapi.middleware.cors import CORSMiddleware
import os
from io import BytesIO

app = FastAPI()

# Configure CORS
origins = ["*"]  # Replace "*" with the specific origins you want to allow
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def generate_contract(client_name: str) -> Document:
    # Load the Word document template
    template_path = os.path.abspath('tomp.docx')
    doc = Document(template_path)

    # Replace placeholders with actual values
    for paragraph in doc.paragraphs:
        replace_text(paragraph, '{name}', client_name)

    return doc

def replace_text(paragraph, placeholder, value):
    if placeholder in paragraph.text:
        for run in paragraph.runs:
            run.text = run.text.replace(placeholder, value)

@app.get('/generate-contract', response_class=StreamingResponse)
async def generate_contract_api(client_name: str):
    filled_contract = generate_contract(client_name)

    # Save the filled contract to a BytesIO stream
    stream = BytesIO()
    filled_contract.save(stream)
    stream.seek(0)

    response = StreamingResponse(
        content=stream,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
    response.headers["Content-Disposition"] = "attachment; filename=filled_contract.docx"

    return response
