
from queue import Empty
import time


def run_dl_dimulator(input_queue, delay, callback, stop_event, publish_event, settings, motion_detected_event):
    while not stop_event.is_set():
        try:
            motion_detected_event.wait()
            callback("ON", publish_event, settings, True)
            time.sleep(10)
            callback("OFF", publish_event, settings, True)
            motion_detected_event.clear()

            # action = input_queue.get(timeout=1)
            # if action == "turn_on":
            #     callback("ON", publish_event, settings)
            # elif action == "turn_off":
            #     callback("OFF", publish_event, settings)
        except Empty:
            pass
        time.sleep(delay)
