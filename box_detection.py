import os
from pprint import PrettyPrinter
import cv2
import numpy as np
from document_generator import DocumentGenerator
from file_server import FileServer
import uuid

from get_signed_access_url import get_presigned_access_url
from mps_handler import MPSHandler

BUCKET = 'hammerspace-image-buckettest'
MATHPIXSNIP_KEY = 'b99b5f212bc410ba06aa95ed714251a1fabc4efbedc25ebe47fbd77a5f977e1f'
D_BUCKET = 'hammerspace-download-bucket'

def create_mapping(rects):
    mapping = {}
    i = 1
    for (x,y,w,h) in rects:
        if i % 10 == 0:
            i += 1
        text = "KARL" + str(i)
        mapping[text] = (x,y,w,h)  
        i += 1
    return mapping

def create_boxes(image, mapping: dict):
    """
    MUTATES IMAGE
    """
    for text, (x,y,w,h) in mapping.items():
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,255), -1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        max_font_scale = 10
        font_thickness = 4
        while max_font_scale > 0:
            text_size = cv2.getTextSize(text, font, max_font_scale, font_thickness)[0]
            if text_size[0] <= (w) and text_size[1] <= (h):
                break
            max_font_scale -= 1
        font_color = (0, 0, 0)
        # Calculate text size and position to center it on the rectangle
        text_size = cv2.getTextSize(text, font, max_font_scale, 2)[0]
        text_x = (x)
        text_y = (y + 2 * (h // 3))

        cv2.putText(image, text, (text_x, text_y), font, max_font_scale, font_color, font_thickness)

def save_math_images(image, uid: str, mapping: dict):
    for text, (x,y,w,h) in mapping.items():
        img = image[y:y+h, x:x+w]
        os.makedirs('./math_saves', exist_ok=True)
        cv2.imwrite(f'./math_saves/{uid}-{text}.jpg', img)

def upload_math_images(uid: str, mapping: dict):
    fs = FileServer()
    for text, _ in mapping.items():
        fs.Upload(f'math_saves/{uid}-{text}.jpg', 'jpg', BUCKET)

def send_to_mathpix(uid: str, mapping: dict):
    pprint = PrettyPrinter()
    handler = MPSHandler(MATHPIXSNIP_KEY)
    translations = {}
    for text, _ in mapping.items():
        fileid = f'{uid}-{text}.jpg'
        presigned_url = get_presigned_access_url(fileid, BUCKET)
        translated = handler.GetTranslation(presigned_url)

        if type(translated) is dict:
            print(translated)
            exit(1)
        translated = handler.postprocess(translated)
        translations[text] = translated
    pprint.pprint(translations)
    return translations
    
def save_text_image(image, uid):
    os.makedirs('./math_saves', exist_ok=True)
    cv2.imwrite(f'./math_saves/{uid}.jpg', image)

def upload_text_image(uid: str):
    fs = FileServer()
    fs.Upload(f'math_saves/{uid}.jpg', 'jpg', BUCKET)

def send_text_to_mathpix(uid: str):
    pprint = PrettyPrinter()
    handler = MPSHandler(MATHPIXSNIP_KEY)
    fileid = f'{uid}.jpg'
    presigned_url = get_presigned_access_url(fileid, BUCKET)
    translated = handler.GetTranslation(presigned_url)
    if type(translated) is dict:
        print(translated)
        exit(1)
    translated = handler.postprocess(translated)
    pprint.pprint(translated)    
    return translated







image = cv2.imread('2.jpeg')
blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
rects = []
for i, c in enumerate(cnts):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)
    if len(approx) == 4:
        x,y,w,h = cv2.boundingRect(approx)
        if min(w, h) > 10:
            rects.append((x,y,w,h))

# parsing math
mapping = create_mapping(rects)
print(mapping)
uid = uuid.uuid4() # REPLACE THIS WITH ID OF ACTUAL IMAGE
save_math_images(image, uid, mapping)
upload_math_images(uid, mapping)
translations = send_to_mathpix(uid, mapping)

# parse text
create_boxes(image, mapping)
save_text_image(image, uid)
upload_text_image(uid)
final_translated = send_text_to_mathpix(uid)
for text, new in translations.items():
    print(text, new)
    final_translated = final_translated.replace(text, new)
print(final_translated)

fileid = f'{uid}-final'
file_store = FileServer()
generator = DocumentGenerator()    

output_file = generator.GenerateTEX(fileid, final_translated)
generator.GeneratePDF(output_file)
pdf_filename = output_file.rsplit('.', 1)[0] + ".pdf"
tex_obj = file_store.Upload(output_file, "tex", D_BUCKET)
pdf_obj = file_store.Upload(pdf_filename, "pdf", D_BUCKET)

tex_url = get_presigned_access_url(tex_obj, D_BUCKET)
pdf_url = get_presigned_access_url(pdf_obj, D_BUCKET)

print({
    'pdf_url': pdf_url,
    'tex_url': tex_url
})



cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.waitKey()