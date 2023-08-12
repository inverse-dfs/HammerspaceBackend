import os
import cv2
import numpy as np

def create_mapping(rects):
    mapping = {}
    for i, (x,y,w,h) in enumerate(rects):
        text = "KARL" + str(i)
        mapping[text] = (x,y,w,h)  
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

def save_math_images(image, mapping: dict):
    for text, (x,y,w,h) in mapping.items():
        img = image[y:y+h, x:x+w]

        os.makedirs('./math_saves', exist_ok=True)
        cv2.imwrite(f'./math_saves/{text}.jpg', img)

image = cv2.imread('2.jpeg')
blur = cv2.pyrMeanShiftFiltering(image, 11, 21)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
k = 0
rects = []
for i, c in enumerate(cnts):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.015 * peri, True)
    if len(approx) == 4:
        x,y,w,h = cv2.boundingRect(approx)
        if min(w, h) > 10:
            rects.append((x,y,w,h))
mapping = create_mapping(rects)
print(mapping)
save_math_images(image, mapping)
create_boxes(image, mapping)

cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.waitKey()