import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

green = 12
GPIO.setup(green, GPIO.OUT)

status = sys.argv[1]

GPIO.output(green, status)
