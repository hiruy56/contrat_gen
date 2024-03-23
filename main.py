from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from docx import Document
import os
from io import BytesIO

app = FastAPI()

def generate_contract(client_name: str, date1: str, date: str, nationality: str, telephone: str, price: str, date2: str, datepay: str, date3: str, name1: str) -> Document:
    # Replace this with the actual path to your template document
    template_path = os.path.abspath('tomp.docx')
    doc = Document(template_path)

    # Replace placeholders with actual values
    replacements = {
        '{name}': client_name,
        '{date1}': date1,
        '{date}': date,
        '{nationality}': nationality,
        '{telephone}': telephone,
        '{price}': price,
        '{date2}': date2,
        '{datepay}': datepay,
        '{date3}': date3,
        '{name1}': name1
    }
    
    for paragraph in doc.paragraphs:
        replace_text(paragraph, replacements)

    return doc


def replace_text(paragraph, replacements):
    for run in paragraph.runs:
        for placeholder, value in replacements.items():
            run.text = run.text.replace(placeholder, value)

@app.get('/generate-contract', response_class=StreamingResponse)
async def generate_contract_api(
    name: str,
    date0: str,
    date: str,
    nationality: str,
    telephone: str,
    price: str,
    date1: str,
    datepay: str,
    date2: str,
    date3: str,
    name1: str
):
    filled_contract = generate_contract(name, date0, date, nationality, telephone, price, date1, datepay, date2, date3, name1)

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
