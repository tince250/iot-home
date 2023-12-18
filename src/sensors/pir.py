import RPi.GPIO as GPIO
import time

from components.pir import motion_detected_callback, no_motion_detected_callback

class PIR(object):
    def __init__(self, settings):
        self.pin = settings['port']
        self.name = settings['name']

    def detect_motion(self, publish_event, settings):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda x: motion_detected_callback(publish_event, settings))
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=lambda x: no_motion_detected_callback(publish_event, settings))


def run_pir_loop(pir, stop_event, publish_event, settings):
    pir.detect_motion(publish_event, settings)
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(pir.pin)
            GPIO.cleanup()
            break