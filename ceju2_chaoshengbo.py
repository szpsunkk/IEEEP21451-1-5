import RPi.GPIO as GPIO
import time

print("Distence Measurement In Progress")

GPIO.setmode(GPIO.BCM)

TRIG = 17
ECHO = 27
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

GPIO.output(TRIG, True)
time.sleep(0.001)
GPIO.output(TRIG, False)
while True:
	while GPIO.input(ECHO) == 0:
		pass
	pulse_start = time.time()

	while GPIO.input(ECHO) == 1:
		pass
	pulse_end = time.time()

	puluse_duration = pulse_end - pulse_start
	distence  = puluse_duration * 17150
	distence = round(distence, 2)
	print("distence: {}cm".format(distence))
GPIO.cleanup()