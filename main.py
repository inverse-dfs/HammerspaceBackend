from typing import Union
import logging
from fastapi import FastAPI, HTTPException
from get_signed_url import get_upload_url

app = FastAPI()

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
