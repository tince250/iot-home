import RPi.GPIO as GPIO
import time
from queue import Empty

class Buzzer(object):
    def __init__(self, pin, sensor_name=""):
        self.pin = pin
        self.name = sensor_name

    def buzz(self, pitch, duration):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)

        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)
        for i in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)
            # if stop_event.is_set():
            #     GPIO.cleanup()
            # break

def run_buzzer_loop(buzzer_queue, buzzer, pitch, duration, delay, buzzer_print_callback, stop_event, publish_event, settings):
    while True:
        try:
            action = buzzer_queue.get(timeout=1)
            if action == "turn_sound_on":
                buzzer.buzz(pitch, duration)
        except Empty:
            pass
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)
