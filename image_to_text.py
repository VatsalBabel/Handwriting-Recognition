import cv2
import pytesseract
from PIL import Image
import numpy as np

cap=cv2.VideoCapture(0)
while cap.isOpened():
        ret,frame=cap.read()
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        blurred4=cv2.GaussianBlur(gray,(21,21),3)       
        thresh4 = cv2.threshold(blurred4,100,200,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]  
        
        kernel = np.ones((5,5),np.uint8)
        thresh4_dilated = cv2.dilate(thresh4, kernel, iterations=1)       
        
        cv2.imshow('window4',thresh4_dilated)
        
        
        cv2.imwrite('capture4.png',thresh4_dilated)
        text4 = pytesseract.image_to_string(Image.open('capture4.png'))
        if len(text4)!=0:
            cv2.imwrite('final.png', thresh4_dilated)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):       
            break
        
text4 = pytesseract.image_to_string(Image.open('final.png'))
print(text4)
cv2.destroyAllWindows(0)
cap.release()