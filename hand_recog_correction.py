# -*- coding: utf-8 -*-
import cv2
import numpy as np
import pytesseract
from PIL import Image,ImageEnhance,ImageFilter
from textblob import TextBlob
from textblob import Word
import nltk


#Capturing the image from camera
cam = cv2.VideoCapture(0)
text=" "
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
        im.save('final.jpg')
        #Reading the image
        text=pytesseract.image_to_string(Image.open('final.jpg'))
        #Getting the text from the image using pytesseract
        if len(text)!=0:
            print(text)
            token=nltk.word_tokenize(text)
            l=len(token)
            list_sugg=[]
            for i in range(0,l):    
                print("...................")
                t_line=TextBlob(token[i])
                w_line=Word(token[i])
                l=w_line.spellcheck()
                length=len(l)
                print("are you looking for")
                for i in range(0,length):
                    print(str(i+1)+"->"+str(l[i][0]))
                
                print("according to me   :"+str(t_line.correct()))
                list_sugg.append(str(t_line.correct()))
            print("according to me......")    
            print(" ".join(list_sugg))
        #'q' for exit
        if cv2.waitKey(1) &0xFF == ord('q'):
            break
    except:
        break

#Exiting
cam.release()
cv2.destroyAllWindows()
