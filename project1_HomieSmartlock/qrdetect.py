import cv2
import pyzbar.pyzbar as pyzbar
import RPi.GPIO as GPIO
import time

cap=cv2.VideoCapture(0)
font=cv2.FONT_HERSHEY_PLAIN

CONTROL_PIN = 17
PWM_FREQ = 50
STEP=95

GPIO.setmode(GPIO.BCM)
GPIO.setup(CONTROL_PIN, GPIO.OUT)

led=27
GPIO.setup(led, GPIO.OUT)

pwm = GPIO.PWM(CONTROL_PIN, PWM_FREQ)
pwm.start(0)

def angle_to_duty_cycle(angle=0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

while True:
   
    a=0
    GPIO.output(led,GPIO.HIGH)
    _, frame=cap.read()
    decodeObjects=pyzbar.decode(frame)
    for obj in decodeObjects:
        cv2.putText(frame,str(obj.data),(50,50),font,2,(0,0,255),3)
        a=str(obj.data)
    cv2.imshow("Frame",frame)
    if a=="b'12345'":
        print("success")
        for angle in range(130, 34, -STEP):
            dc = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            time.sleep(1)
        for angle in range(35, 131, STEP):
            dc = angle_to_duty_cycle(angle)
            pwm.ChangeDutyCycle(dc)
            time.sleep(1)
        pwm.stop()
        GPIO.cleanup()
        cv2.destroyAllWindows()
        break
        time.sleep(5)
    key=cv2.waitKey(1)
    if key==27:
        GPIO.output(led,GPIO.LOW)
        cv2.destroyAllWindows()
        break
