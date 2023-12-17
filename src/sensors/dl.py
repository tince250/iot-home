import RPi.GPIO as GPIO
import time
from queue import Empty

class DL(object):
    def __init__(self, pin, sensor_name="") -> None:
        self.pin = pin
        self.name = sensor_name
        self.status = "OFF"
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
    
    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.status = "ON"

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.status = "OFF"

def run_dl_loop(input_queue, dl, delay, callback, stop_event, publish_event, settings):
    while True:
        try:
            action = input_queue.get(timeout=1)
            status_changed = False
            if action == "turn_on" and dl.status == "OFF":
                dl.turn_on()
                status_changed = True
            elif action == "turn_off" and dl.status == "ON":
                dl.turn_off()
                status_changed = True

            if status_changed:
                callback(dl.status, publish_event, settings)
        except Empty:
            pass

        if stop_event.is_set():
            GPIO.cleanup()
            break

        time.sleep(delay)
