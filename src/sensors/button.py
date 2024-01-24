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
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback = lambda x: self.button_callback(self.name), bouncetime = 200)

def run_button_loop(button, stop_event, callback, publish_event, settings):
    #button.detect_button_press(publish_event, settings)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(button.pin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
    # previous_value = 0
    current_value = 0
    while True:
        if GPIO.input(button.pin) == GPIO.HIGH and not current_value:
            current_value = 1
            callback(publish_event, settings, current_value == 1)
        elif GPIO.input(button.pin) == GPIO.LOW and current_value:
            current_value = 0
            callback(publish_event, settings, current_value == 1)
        # if current_value != previous_value:
        #     previous_value = current_value
        #     callback(publish_event, settings, current_value == 1)
        # else:
        #     continue
        time.sleep(0.5)
        if stop_event.is_set():
            GPIO.remove_event_detect(button.pin)
            GPIO.cleanup()
            break
