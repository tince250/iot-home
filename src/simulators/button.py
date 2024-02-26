import random
import time

def generate_values(delay, stop_event):
    value = 0
    previous_value = None
    while True:
        time.sleep(delay)
        value = random.randint(0,1) == 1
        # value = 0
        if value != previous_value:
            previous_value = value
            yield value
        else:
            continue
        if stop_event.is_set():
            break
        # if value < 0:
        #     value = 0
        # if value > 1:
        #     value = threshold
        # value += random.uniform(-0.5, 0.5)
        # yield value

def run_button_simulator(delay, callback, stop_event, publish_event, settings, threshold=0.6):
    for value in generate_values(delay=1, stop_event=stop_event):
        # print(value)
        callback(publish_event, settings, value == 1)
        if stop_event.is_set():
            break