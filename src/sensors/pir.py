import RPi.GPIO as GPIO
import time

class PIR(object):
    def __init__(self, pin, motion_detected_callback, no_motion_callback):
        self.pin = 4
        self.motion_detected_callback = motion_detected_callback
        self.no_motion_callback = no_motion_callback

    def detect_motion(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=self.motion_detected_callback)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=self.no_motion_callback)


def run_pir_loop(pir, stop_event):
    pir.detect_motion()
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(pir.pin)
            break