import RPi.GPIO as GPIO
import time
from locks import print_lock

class Button(object):
    def __init__(self, pin, sensor_name=""):
        self.pin = pin
        self.name = sensor_name

    def button_callback(self, event):
        with print_lock: 
            print(f"{self.name} is clicked!")

    def detect_button_press(self, publish_event, settings):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = lambda x: self.button_callback(self.name), bouncetime = 100)

def run_button_loop(button, stop_event, publish_event, settings):
    button.detect_button_press(publish_event, settings)
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(button.pin)
            GPIO.cleanup()
            break
