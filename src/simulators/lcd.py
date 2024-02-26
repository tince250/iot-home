
from queue import Empty
import time
import random

def run_lcd_simulator(delay, callback, stop_event, settings, display_values_event, data_queue):
    while not stop_event.is_set():
        try:
            display_values_event.wait()
            temperature, humidity = data_queue.get(timeout=1)
            display_values_event.clear()
            callback(temperature, humidity, settings, True)
        except Empty:
            pass
        time.sleep(delay)
