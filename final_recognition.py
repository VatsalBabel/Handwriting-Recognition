import sys
import cv2
import numpy as np
import pytesseract
from textblob import Word
from PIL import Image,ImageEnhance,ImageFilter

#Capturing the image from camera
cam = cv2.VideoCapture(0)

while True:
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
        cv2.imwrite(r'/home/vatsalbabel/Desktop/capture.png',thresh_dilated)
        #Reading the image
        im=Image.open(r'/home/vatsalbabel/Desktop/capture.png')
        #Filtering the noise and enhancing the image
        im=im.filter(ImageFilter.MedianFilter())
        enhancer=ImageEnhance.Contrast(im)
        im=enhancer.enhance(5)
        im=im.convert('1')
        #Saving the image
        im.save(r'/home/vatsalbabel/Desktop/final.jpg')
        #Reading the image
        toString_image = Image.open(r'/home/vatsalbabel/Desktop/final.jpg')
        #Getting the text from the image using pytesseract
        recogs = pytesseract.image_to_string(toString_image)
        
        #Showing the confidence percentage and suggestion
        if len(str(recogs))!=0:
            recogs = recogs.lower()
            recogs = recogs.strip()
            recogs = recogs.replace('\\',' ')
            
            #Suggestion module
            try:
                list_sugg = []
                list_of_words = recogs.split()
                for i in list_of_words:
                    word = Word(i)
                    list_sugg.append(str(word.spellcheck()[0][0]))
                recogs = " ".join(list_sugg)
            except:
                pass
            sys.stdout.write(recogs)
            
            #Confidence module
            recogs = recogs.strip()
            recogs = recogs.replace('\\',' ')
            list_of_words = str(recogs).split()
            confidence_per = 0
            count = 0
            for i in list_of_words:
                try:
                    word = Word(str(i))
                    confidence_per += float(word.spellcheck()[0][1])
                    count += 1
                    confidence_per /= count
                except:
                    pass
                
            #sys.stdout.write("\tConfidence Level: "+str(confidence_per*100))
            print
        #'q' for exit
        if cv2.waitKey(1) &0xFF == ord('q'):
            break

#Exiting
cam.release()
cv2.destroyAllWindows()