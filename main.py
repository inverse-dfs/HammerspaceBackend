from typing import Union
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from get_signed_url import get_upload_url
from get_signed_access_url import get_presigned_access_url
from mps_handler import MPSHandler
from document_generator import DocumentGenerator
from file_server import FileServer

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
def read_root():
    return {"Hello": "World"}

@app.get("/presigned")
def presigned_url():
    response = get_upload_url()
    print("response", response)    
    if response is None:
        raise HTTPException(status_code=500, detail="Could not generate presigned url") 
    return response 

class TranslationRequest(BaseModel):
    fileid: str

@app.post("/translate")
def translation_request(item: TranslationRequest):
    try:
        handler = MPSHandler()
    except KeyError as e:
        raise HTTPException(status_code=500, detail="Unable to Access MathPixSnip API")
    presigned_url = get_presigned_access_url(item.fileid)
    translated = handler.GetTranslation(presigned_url)
    generator = DocumentGenerator()
    output_file = generator.GenerateTEX(item.fileid, translated)
    generator.GeneratePDF(output_file)
    file_store = FileServer()
    pdf_filename = output_file.rsplit('.', 1)[0] + ".pdf"
    file_store.Upload(output_file, "tex")
    file_store.Upload(pdf_filename, "pdf")
    return output_file
