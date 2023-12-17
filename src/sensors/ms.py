import RPi.GPIO as GPIO
import time

class MS(object):

    def __init__(self, **kwargs) -> None:
        self.r1 = kwargs["R1"]
        self.r2 = kwargs["R2"]
        self.r3 = kwargs["R3"]
        self.r4 = kwargs["R4"]
        self.c1 = kwargs["C1"]
        self.c2 = kwargs["C2"]
        self.c3 = kwargs["C3"]
        self.c4 = kwargs["C4"]
        self.name = kwargs["sensor_name"]

    # TODO: ako nista ne pritisne da kazemo da nis nije pritisnuto ili nista da ne prikazujemo?
    def check_row(self, row, characters):
        GPIO.output(row, GPIO.HIGH)
        if(GPIO.input(self.c1) == 1):
            return characters[0]
        if(GPIO.input(self.c2) == 1):
            return characters[1]
        if(GPIO.input(self.c3) == 1):
            return characters[2]
        if(GPIO.input(self.c4) == 1):
            return characters[3]
        GPIO.output(row, GPIO.LOW)

        return None

    def get_pressed_key(self):       
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.r1, GPIO.OUT)
        GPIO.setup(self.r2, GPIO.OUT)
        GPIO.setup(self.r3, GPIO.OUT)
        GPIO.setup(self.r4, GPIO.OUT)

        GPIO.setup(self.c1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.c2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.c3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.c4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        pressed_key = (
            self.check_row(self.r1, ["1", "2", "3", "A"]) or
            self.check_row(self.r2, ["4", "5", "6", "B"]) or
            self.check_row(self.r3, ["7", "8", "9", "C"]) or
            self.check_row(self.r4, ["*", "0", "#", "D"])
        )

        return pressed_key

def run_ms_loop(ms, delay, callback, stop_event, settings, publish_event):
    while True:
        pressed_key = ms.get_pressed_key()
        if pressed_key:
            callback(pressed_key, settings, publish_event)
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)
