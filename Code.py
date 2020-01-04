import time, datetime
import telepot
from telepot.loop import MessageLoop
import os
import RPi.GPIO as GPIO
from gpiozero import Buzzer
from time import sleep

buzzer = Buzzer(24)


#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 23
 
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(24, GPIO.OUT) #BUzzer
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
def cam():
    os.system('fswebcam --no-banner imagetest')#For clicking Pic

def action():
    cam()
    message = "Someone's at the door !!!"
    telegram_bot.sendMessage (761084539, message) # Add Chat ID
    telegram_bot.sendPhoto(761084539,photo=open("imagetest"))
 
if __name__ == '__main__':
    while True:
        dist=distance()
        print(dist)
        if dist<20:
            GPIO.output(24, True)
            time.sleep(0.5) 
            GPIO.output(24, False)
            print("Motion Detected...")
            telegram_bot = telepot.Bot('850662582:AAFZYs11fR_II-m7OAj2oGyhsiSqnz-PgwI')# Token ID 
            buzzer.beep()#Buzzer turns on
            action()

            MessageLoop(telegram_bot, action)
            print('Running Perfectly fine !!!')
            buzzer.off()#Buzzer turns off
            sleep(1)
        time.sleep(1)