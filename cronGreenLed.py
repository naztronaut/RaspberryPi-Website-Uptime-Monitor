import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

green = 12
GPIO.setup(green, GPIO.OUT)

if sys.argv[1] == "HIGH":
    status = GPIO.HIGH
else:
    status = GPIO.LOW

GPIO.output(green, status)
