import cv2
import uuid
import os

class ImageSegmenter:
    def __init__(self, file_path):
        self.image = cv2.imread(file_path)
        self.blur = cv2.pyrMeanShiftFiltering(self.image, 11, 21)
        self.gray = cv2.cvtColor(self.blur, cv2.COLOR_BGR2GRAY)
        self.thresh = cv2.threshold(self.gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        self.__get_mappings()
        self.uid = uuid.uuid4()

    def create_boxes(self):
        """
        MUTATES IMAGE
        """
        for text, (x,y,w,h) in self.mapping.items():
            cv2.rectangle(self.image,(x,y),(x+w,y+h),(255,255,255), -1)
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
            cv2.putText(self.image, text, (text_x, text_y), font, max_font_scale, font_color, font_thickness)

    def __create_mappings(self, rects):
        mapping = {}
        i = 1
        for (x,y,w,h) in rects:
            if i % 10 == 0:
                i += 1
            text = "KARL" + str(i)
            mapping[text] = (x,y,w,h)  
            i += 1
        return mapping

    def __get_mappings(self):
        cnts = cv2.findContours(self.thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
        self.mapping = self.__create_mappings(rects)
    
    def save_math_imgs(self):
        for text, (x,y,w,h) in self.mapping.items():
            img = self.image[y:y+h, x:x+w]
            os.makedirs('./tmp', exist_ok=True)
            cv2.imwrite(f'./tmp/{self.uid}-{text}.jpg', img)

    def save_text_imgs(self):
        os.makedirs('./tmp', exist_ok=True)
        cv2.imwrite(f'./tmp/{self.uid}.jpg', self.image)
    

        