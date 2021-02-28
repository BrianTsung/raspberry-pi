#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import os, signal, subprocess
import sys 
from pyzbar.pyzbar import decode
import cv2
import RPi.GPIO as GPIO
import time



def doReMi():
    TRUE=1
    GPIO.setmode(GPIO.BCM)
    BeepPin = 12
    GPIO.setup(BeepPin, GPIO.OUT)
    GPIO.output(BeepPin, GPIO.HIGH)
    time.sleep(2)
    GPIO.cleanup()


CONTROL_PIN = 17
PWM_FREQ = 50
STEP=95

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

def qrcode():
    os.system("fswebcam homie.png")
    
    image=cv2.imread("/home/pi/Desktop/homie.png") 
    result = decode(image) 
    for item in result:
        print (item.type, item.data.decode("utf-8")) 
        if item.data.decode("utf-8")=="12345":
            for angle in range(130, 34, -STEP):
                dc = angle_to_duty_cycle(angle)
                pwm.ChangeDutyCycle(dc)
                time.sleep(1)
            for angle in range(35, 131, STEP):
                dc = angle_to_duty_cycle(angle)
                pwm.ChangeDutyCycle(dc)
                time.sleep(1)
        elif item.data.decode("utf-8")!="12345":
            doReMi()
        
true=1           
buttonpin=24
GPIO.setup(buttonpin, GPIO.IN)
while (true==1):
    inputvalue=GPIO.input(buttonpin)
    if inputvalue==False:
        print("ok")
        qrcode()

            
#qrcode()
pwm.stop()
GPIO.cleanup()








