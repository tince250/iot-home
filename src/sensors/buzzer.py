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

def run_buzzer_loop(alarm_clock_queue, buzzer, pitch, duration, delay, alarm_clock_on_event, alarm_clock_off_event, buzzer_print_callback, stop_event, publish_event, settings):
    current_clock_alarm = None
    called_callback = False
    while True:
        if alarm_clock_on_event:
            while not alarm_clock_off_event.is_set():
                try:
                    current_clock_alarm = alarm_clock_queue.get(timeout=1)
                except Empty:
                    pass
                if current_clock_alarm and is_after_current_time(current_clock_alarm['date'], current_clock_alarm['time']):
                    if not alarm_clock_on_event.is_set():
                        alarm_clock_on_event.set()
                    if not called_callback:
                        buzzer_print_callback(publish_event, settings, status="ON")
                        called_callback = True
                    buzzer.buzz(pitch, duration)

            if current_clock_alarm:
                called_callback = False
                buzzer_print_callback(publish_event, settings, status="OFF")
            current_clock_alarm = None
        
        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)

def is_after_current_time(date_str, time_str):
    from datetime import datetime
    target_datetime = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
    current_datetime = datetime.now().replace(second=0, microsecond=0)
    return current_datetime >= target_datetime
