import cv2
import numpy as np
import pytesseract
from PIL import Image,ImageEnhance,ImageFilter

#Capturing the image from camera
cam = cv2.VideoCapture(0)

while True:
    try:
        ret, frame = cam.read()
        #Converting image to gray
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #Applying Threshold
        thresh = cv2.threshold(gray,100,200,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        #Setting the kernel
        kernel = np.ones((5,5),np.uint8)
        #Dilating
        thresh_dilated = cv2.dilate(thresh, kernel, iterations=0)   
        #Displaying the window for camera
        cv2.imshow('window',thresh_dilated)
        #Saving the image
        cv2.imwrite('capture.png',thresh_dilated)
        #Reading the image
        im=Image.open('capture.png')
        #Filtering the noise and enhancing the image
        im=im.filter(ImageFilter.MedianFilter())
        enhancer=ImageEnhance.Contrast(im)
        im=enhancer.enhance(5)
        im=im.convert('1')
        #Saving the image
        im.save(r'/home/vatsalbabel/Desktop/newfile/final.jpg')
        #Reading the image
        toString_image = Image.open(r'/home/vatsalbabel/Desktop/newfile/final.jpg')
        #Getting the text from the image using pytesseract
        print(pytesseract.image_to_string(toString_image))
        #'q' for exit
        if cv2.waitKey(1) &0xFF == ord('q'):
            break
    except:
        break

#Exiting
cam.release()
cv2.destroyAllWindows()