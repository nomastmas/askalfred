"""
switch actions for alfred
"""
import re
import RPi.GPIO as GPIO 

# constants for GPIO pins
LIGHTS = 7

def _init_gpio():
    # use board pin numbering
    GPIO.setmode(GPIO.BOARD)     

    GPIO.setwarnings(False)
    GPIO.setup(LIGHTS, GPIO.OUT)     

def handler(message, alfred):
    _init_gpio()
    if (re.search("lights", message)):
        if (re.search("on", message)):
            GPIO.output(LIGHTS, True)
        elif (re.search("off", message)):
            GPIO.output(LIGHTS, False)
