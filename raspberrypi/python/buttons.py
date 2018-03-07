import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# GPIO.setup(24, GPIO.OUT)

try:
    while(True):
        button_state = GPIO.input(23)
        if button_state == False:
            print("Ooooo she pressed now")
            time.sleep(0.2)

except:
    GPIO.cleanup()
