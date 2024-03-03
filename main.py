from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from docx import Document
import os
from io import BytesIO
from datetime import datetime  # Import the datetime module

app = FastAPI()


def generate_contract(client_name: str, date: str, nationality: str, telephone: str, price: str) -> Document:
    # Load the Word document template
    template_path = os.path.abspath('tomp.docx')
    doc = Document(template_path)

    # Replace placeholders with actual values
    for paragraph in doc.paragraphs:
        replace_text(paragraph, '{name}', client_name)
        replace_text(paragraph, '{date}', date)
        replace_text(paragraph, '{nationality}', nationality)
        replace_text(paragraph, '{telephone}', telephone)
        replace_text(paragraph, '{price}', price)

    return doc

def replace_text(paragraph, placeholder, value):
    if placeholder in paragraph.text:
        for run in paragraph.runs:
            run.text = run.text.replace(placeholder, value)


@app.get('/generate-contract', response_class=StreamingResponse)
async def generate_contract_api(
    client_name: str,
    date: str,  # Default to current date
    nationality: str,
    telephone: str,
    price: str
):
    filled_contract = generate_contract(client_name, date, nationality, telephone, price)

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
