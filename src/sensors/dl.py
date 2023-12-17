import RPi.GPIO as GPIO
import time
from queue import Empty

class DL(object):
    def __init__(self, pin, sensor_name="") -> None:
        self.pin = pin
        self.name = sensor_name
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
    
    # TODO: je l moze ovo za setmode i setup u init
    def turn_on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def turn_off(self):
        GPIO.output(self.pin, GPIO.LOW)

def run_dl_loop(input_queue, dl, delay, callback, stop_event, publish_event, settings):
    while True:
        try:
            action = input_queue.get(timeout=1)
            status = "OFF"
            if action == "turn_on":
                dl.turn_on()
                status = "ON"
            elif action == "turn_off":
                dl.turn_off()

            callback(status, publish_event, settings)
        except Empty:
            pass

        if stop_event.is_set():
            GPIO.cleanup()
            break

        time.sleep(delay)
