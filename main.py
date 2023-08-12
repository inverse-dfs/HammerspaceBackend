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
from format_injector import FormatInjector
from pdf_converter import convert_to_jpg
from create_user import insert_user
from verify_login import verify_login
from image_segmentation import ImageSegmenter

from contextlib import asynccontextmanager
from config import Config

    
config = Config()
app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/presigned")
def presigned_url():
    response = get_upload_url(config.image_bucket) # todo: add file type specifier to this api call
    print("response", response)    
    if response is None:
        raise HTTPException(status_code=500, detail="Could not generate presigned url") 
    return response 

class LoginRequest(BaseModel):
    username: str
    password: str
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

@app.post("/login")
def login(item: LoginRequest):
    return verify_login(item.username, item.password)

@app.post("/signup")
def singup(item: SignupRequest):
    res = insert_user(item.username, item.email, item.password)
    return res

class TranslationRequest(BaseModel):
    fileid: str

@app.post("/translate")
def translation_request(item: TranslationRequest):
    handler = MPSHandler(config.mathpixsnip_key)
   
    file_store = FileServer()
    fileid = item.fileid
    ext = fileid.rsplit('.', 1)

    # if len(ext) >=2 and ext[-1] == 'pdf':
    #     file_store.Download(fileid)
    #     conv_name = convert_to_jpg(fileid)
    #     file_store.Upload(conv_name, "jpeg", bucket=config.image_bucket)
    #     fileid = conv_name

    file_store.Download(fileid, config.image_bucket, path='tmp/')
    segmenter = ImageSegmenter(f'tmp/{fileid}', config)
    segmenter.save_math_imgs()
    segmenter.upload_math_imgs()
    segmenter.save_text_imgs()
    segmenter.upload_text_img()
    maths_translations = segmenter.send_to_mathpix()
    processed_text = segmenter.send_text_to_mathpix()
    for text, new in maths_translations.items():
        processed_text = processed_text.replace(text, new)
    uid = segmenter.uid
    fileid = f'{uid}-final'
    file_store = FileServer()
    generator = DocumentGenerator()    
    output_file = generator.GenerateTEX(fileid, processed_text)
    generator.GeneratePDF(output_file)
    pdf_filename = output_file.rsplit('.', 1)[0] + ".pdf"
    tex_obj = file_store.Upload(output_file, "tex", config.download_bucket)
    pdf_obj = file_store.Upload(pdf_filename, "pdf", config.download_bucket)

    tex_url = get_presigned_access_url(tex_obj, config.download_bucket)
    pdf_url = get_presigned_access_url(pdf_obj, config.download_bucket)

    print({
        'pdf_url': pdf_url,
        'tex_url': tex_url
    })
    #save the 

    # presigned_url = get_presigned_access_url(fileid, config.image_bucket)
    # translated = handler.GetTranslation(presigned_url)
    # if type(translated) is dict:
    #     print(translated)
    #     raise HTTPException(status_code=500, detail=str(translated)) 
    # translated = handler.postprocess(translated)

    # injector = FormatInjector()
    # injected = injector.run(translated)
    # if injected == '':
    #     print(translated)
    #     raise HTTPException(status_code=500, detail="Something went wrong with latex injection. The input was probably poorly formatted.") 
    
    # generator = DocumentGenerator()    
    # output_file = generator.GenerateTEX(fileid, injected)
    # generator.GeneratePDF(output_file)
    # pdf_filename = output_file.rsplit('.', 1)[0] + ".pdf"
    # tex_obj = file_store.Upload(output_file, "tex", config.download_bucket)
    # pdf_obj = file_store.Upload(pdf_filename, "pdf", config.download_bucket)
    
    # tex_url = get_presigned_access_url(tex_obj, config.download_bucket)
    # pdf_url = get_presigned_access_url(pdf_obj, config.download_bucket)
    # return {
    #     'pdf_url': pdf_url,
    #     'tex_url': tex_url
    # }
