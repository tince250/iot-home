import RPi.GPIO as GPIO
import time

class PIR(object):
    def __init__(self, pin, motion_detected_callback, no_motion_callback, sensor_name=""):
        self.pin = pin
        self.motion_detected_callback = lambda name: print("move" + name)
        self.no_motion_callback = lambda name: print("no move" + name)
        self.name = sensor_name

    def detect_motion(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        # GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda x: self.motion_detected_callback(self.name))
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=lambda x: self.no_motion_callback(self.name))


def run_pir_loop(pir, stop_event):
    pir.detect_motion()
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(pir.pin)
            GPIO.cleanup()
            break