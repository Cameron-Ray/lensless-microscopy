import RPi.GPIO as GPIO
from time import sleep

LED_Pin = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_Pin, GPIO.OUT)
print("setup done")

while True:
    GPIO.output(LED_Pin, 1)
    sleep(1)
    GPIO.output(LED_Pin, 0)
    sleep(1)
    
    print("toggle")
    
