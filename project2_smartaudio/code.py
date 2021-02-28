import os
import cv2
import numpy as np
from keras.models import model_from_json
from keras.preprocessing import image
import pygame
import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)         
buttonpin=4
buttonpin2=3
buttonpin3=18
GPIO.setup(buttonpin, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonpin2, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(buttonpin3, GPIO.IN,pull_up_down=GPIO.PUD_UP)
buttontime=0
playorstop=0

#load model
model = model_from_json(open("/home/pi/Desktop/emotion_detection/fer3.json", "r").read())
#load weights
model.load_weights('/home/pi/Desktop/emotion_detection/fer3.h5')

face_haar_cascade = cv2.CascadeClassifier('/home/pi/Desktop/emotion_detection/haarcascade_frontalface_default.xml')
predicted_emotion =""
while True:
    inputvalue=GPIO.input(buttonpin)
    inputvalue2=GPIO.input(buttonpin2)
    inputvalue3=GPIO.input(buttonpin3)
    if inputvalue==0:
        time.sleep(0.2)
        print("open camara")
        cap = cv2.VideoCapture(0)
        pygame.mixer.init()
        pygame.mixer.music.stop()
        musicno = 1
        inputvalue=1
        while(1):
            inputvalue=GPIO.input(buttonpin)
            # get a frame
            ret, frame = cap.read()
            # show a frame
            cv2.imshow("capture", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if inputvalue==0:
                path = "/home/pi/Desktop/emotion_detection/photo"
                if not os.path.isdir(path):
                    os.mkdir(path)
                gray_img= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces_detected = face_haar_cascade.detectMultiScale(gray_img, 1.2, 4)
                for (x,y,w,h) in faces_detected:
                    cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),thickness=7)
                    roi_gray=gray_img[y:y+w,x:x+h]#cropping region of interest i.e. face area from  image
                    roi_gray=cv2.resize(roi_gray,(48,48))
                    img_pixels = image.img_to_array(roi_gray)
                    img_pixels = np.expand_dims(img_pixels, axis = 0)
                    img_pixels /= 255
                        
                    predictions = model.predict(img_pixels)

                    #find max indexed array
                    print(predictions)
                    max_index = np.argmax(predictions[0])

                    emotions = ('angry', 'happy', 'sad')
                    """global predicted_emotion """
                    predicted_emotion = emotions[max_index]
                    print(predicted_emotion)
                    url="/home/pi/Desktop/emotion_detection/photo/"+str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))+"_"+predicted_emotion+".jpeg"
                    cv2.imwrite(url, frame)
                    if predicted_emotion=="angry":
                        mood="/home/pi/Desktop/emotion_detection/music/angry/"
                    elif predicted_emotion=="happy":
                        mood="/home/pi/Desktop/emotion_detection/music/happy/"
                    elif predicted_emotion=="sad":
                        mood="/home/pi/Desktop/emotion_detection/music/sad/"
                    fileMusic=mood+str(musicno)+".mp3"
                    pygame.mixer.music.load(fileMusic)
                break
                
        
            
        cap.release()
        cv2.destroyAllWindows()
        pygame.mixer.music.play()
    
    
    """print(pygame.mixer.get_busy())"""
    """if predicted_emotion!="":
        musicno+=1
        print(predicted_emotion)
        print(musicno)
        if predicted_emotion=="angry":
            fileMusic="./music/angry/"+str(musicno)+".mp3"
            if musicno>14:
                musicno=14
                fileMusic="./music/angry/1.mp3"
                
        elif predicted_emotion=="happy":
            fileMusic="./music/happy/"+str(musicno)+".mp3"
            if musicno>15:
                musicno=15
                fileMusic="./music/happpy/1.mp3"
                
                
        elif predicted_emotion=="sad":
            fileMusic="./music/sad/"+str(musicno)+".mp3"
            if musicno>17:
                musicno=17
                fileMusic="./music/sad/1.mp3"
        pygame.mixer.music.queue(fileMusic)"""
        
    
    
    if inputvalue2==0:
        time.sleep(0.2)
        if playorstop==1:
            print("play")
            pygame.mixer.music.unpause()
            playorstop=0
        else:
            print("stop")
            pygame.mixer.music.pause()
            playorstop=1
       
    
    starttime=time.time()
    while inputvalue3==0:
        
        inputvalue3=GPIO.input(buttonpin3)
        if inputvalue3==1:
            break
        lasttime=time.time()
        time.sleep(0.2)
        buttontime=lasttime-starttime
        
        if buttontime>0 and buttontime<=0.2:
            print("next")
            buttontime=0
            pygame.mixer.music.stop()
            musicno+=1
            print(musicno)
            if predicted_emotion=="angry":
                if musicno>14:
                    musicno=14
                    fileMusic="/home/pi/Desktop/emotion_detection/music/angry/14.mp3"
                else:
                    fileMusic="/home/pi/Desktop/emotion_detection/music/angry/"+str(musicno)+".mp3"
            if predicted_emotion=="happy":
                if musicno>15:
                    musicno=15
                    fileMusic="/home/pi/Desktop/emotion_detection/music/happpy/15.mp3"
                else:
                    fileMusic="/home/pi/Desktop/emotion_detection/music/happy/"+str(musicno)+".mp3"
            if predicted_emotion=="sad":
                if musicno>17:
                    musicno=17
                    fileMusic="/home/pi/Desktop/emotion_detection/music/sad/17.mp3"
                else:
                    fileMusic="/home/pi/Desktop/emotion_detection/music/sad/"+str(musicno)+".mp3"
            pygame.mixer.music.load(fileMusic)
            pygame.mixer.music.play()
        if buttontime>0.2:
            print("pre")
            buttontime=0
            pygame.mixer.music.stop()
            musicno-=1
            print(musicno)
            if predicted_emotion=="angry":
                if musicno<1:
                    musicno=1
                    fileMusic="/home/pi/Desktop/emotion_detection/music/angry/1.mp3"
                else:
                    fileMusic="/home/pi/Desktop/emotion_detection/music/angry/"+str(musicno)+".mp3"
            if predicted_emotion=="happy":
                if musicno<1:
                    musicno=1
                    fileMusic="/home/pi/Desktop/emotion_detection/music/happy/1.mp3"
                else:
                    fileMusic="/home/pi/Desktop/emotion_detection/music/happy/"+str(musicno)+".mp3"
            if predicted_emotion=="sad":
                if musicno<1:
                    musicno=1
                    fileMusic="/home/pi/Desktop/emotion_detection/music/sad/1.mp3"
                else:
                    fileMusic="/home/pi/Desktop/emotion_detection/music/sad/"+str(musicno)+".mp3"
            pygame.mixer.music.load(fileMusic)
            pygame.mixer.music.play()

        



