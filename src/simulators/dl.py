
from queue import Empty
import time


def run_dl_dimulator(input_queue, delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        try:
            action = input_queue.get(timeout=1)
            if action == "turn_on":
                callback("ON", publish_event, settings)
            elif action == "turn_off":
                callback("OFF", publish_event, settings)
        except Empty:
            pass
        time.sleep(delay)
