import RPi.GPIO as GPIO
import time
from locks import print_lock

class Button(object):
    def __init__(self, port_pin):
        self.port_button = port_pin

    def button_callback(self, event):
        with print_lock: 
            print("Button is clicked!")

    def detect_button_press(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.port_button, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.port_button, GPIO.RISING, callback =
        self.button_callback, bouncetime = 100)

def run_button_loop(button, stop_event):
    button.detect_button_press()
    while True:
        if stop_event.is_set():
            GPIO.remove_event_detect(button.port_button)
            break
