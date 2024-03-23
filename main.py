import tempfile
from fastapi import FastAPI, HTTPException, File, UploadFile
from docx import Document
import os
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI()

def fill_contract_template(contract_details):
    template_path = os.path.abspath('tomp.docx')

    # Load the template document
    doc = Document(template_path)

    # Replace placeholders with actual values
    for paragraph in doc.paragraphs:
        for key, value in contract_details.items():
            if f"{{{key}}}" in paragraph.text:
                paragraph.text = paragraph.text.replace(f"{{{key}}}", str(value))

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for paragraph in cell.paragraphs:
                    for key, value in contract_details.items():
                        if f"{{{key}}}" in paragraph.text:
                            paragraph.text = paragraph.text.replace(f"{{{key}}}", str(value))

    # Save the filled contract to a BytesIO stream
    stream = BytesIO()
    doc.save(stream)
    stream.seek(0)

    return stream

@app.post("/fill-contract")
async def fill_contract(contract_details: dict):
    filled_contract_stream = fill_contract_template(contract_details)
    return StreamingResponse(content=filled_contract_stream, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
