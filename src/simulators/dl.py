
from queue import Empty
import time


def run_dl_dimulator(input_queue, delay, callback, sensor_name, stop_event):
    while not stop_event.is_set():
        try:
            action = input_queue.get(timeout=1)
            if action == "turn_on":
                callback("ON", sensor_name)
            elif action == "turn_off":
                callback("OFF", sensor_name)
        except Empty:
            pass
        time.sleep(delay)
