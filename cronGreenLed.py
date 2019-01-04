import RPi.GPIO as GPIO
import sys
import db

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

green = 12
GPIO.setup(green, GPIO.OUT)

if sys.argv[1] == "HIGH":
    status = GPIO.HIGH
    db.changeLedStatus('green', 1)
else:
    status = GPIO.LOW
    db.changeLedStatus('green', 0)

GPIO.output(green, status)
