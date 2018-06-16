import sys
import cv2
import numpy as np
import pytesseract
from textblob import Word
from PIL import Image,ImageEnhance,ImageFilter
import json
from urllib.parse import urlencode
import urllib.request as urr



#Capturing the image from camera
cam = cv2.VideoCapture(1)
l=[]
while True:
        ret, frame = cam.read()
        #Converting image to gray
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        #Applying Threshold
        thresh = cv2.threshold(gray,70,230,cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
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
        im.save('final.jpg')
        #Reading the image
        toString_image = Image.open('final.jpg')
        #Getting the text from the image using pytesseract
        recogs = pytesseract.image_to_string(toString_image)
        print(recogs)
        l.append(recogs)
        #'q' for exit
        if cv2.waitKey(1) &0xFF == ord('q'):
            break
if(l[0]==l[1] or l[1]==l[2] or l[2]==l[3]):
    start = l[1]+",jaipur"
    finish = "malviya nagar,jaipur"
            
    print(start)     
    print(finish)
    url = 'http://maps.googleapis.com/maps/api/directions/json?%s' % urlencode((('origin', start),('destination', finish)))
    s=urr.urlopen(url)
    ur=s.read() 
    result = json.loads(ur.decode('utf-8'))
    print(type(result))
    #print(result)
    for i in range (0, len (result['routes'][0]['legs'][0]['steps'])):
        j = result['routes'][0]['legs'][0]['steps'][i]['html_instructions']
        print("............................................")
        route=j.replace('<b>',' ').replace('</b>',' ').replace('</div>',' ').replace('<div style="font-size:0.9em">',' ')
        print(route)
#Exiting
cam.release()
cv2.destroyAllWindows()
