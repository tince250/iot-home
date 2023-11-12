import RPi.GPIO as GPIO
import time

class Buzzer(object):
    def __init__(self, pin):
        self.pin = pin

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

def run_buzzer_loop(buzzer, pitch, duration, delay, stop_event):
    while True:
        buzzer.buzz(pitch, duration)
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)
