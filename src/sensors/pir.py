import RPi.GPIO as GPIO
import time

def pir_motion_callback(motion_detected_callback, publish_event, settings, motion_detected_event):
    if motion_detected_event:
        motion_detected_event.set()
    motion_detected_callback(publish_event, settings)

class PIR(object):
    def __init__(self, pin, motion_detected_callback, no_motion_callback, motion_detected_event, publish_event, settings):
        self.pin = pin
        self.motion_detected_callback = motion_detected_callback
        self.no_motion_callback = no_motion_callback
        self.settings = settings
        self.publish_event = publish_event
        self.motion_detected_event = motion_detected_event

    def detect_motion(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        GPIO.add_event_detect(self.pin, GPIO.RISING, callback=lambda x: pir_motion_callback(self.motion_detected_callback, self.publish_event, self.settings, self.motion_detected_event) )
        # GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=lambda x: self.no_motion_callback(self.name))


def run_pir_loop(pir, stop_event):
    pir.detect_motion()
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(pir.pin)
            GPIO.cleanup()
            break