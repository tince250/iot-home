import random
import time

def generate_values(threshold, initial_value=0):
    value = initial_value
    while True:
        if value < 0:
            value = 0
        if value > 1:
            value = threshold
        value += random.uniform(-0.5, 0.5)
        yield value

def run_button_simulator(delay, callback, stop_event, publish_event, settings, threshold=0.6):
    for value in generate_values(threshold=threshold):
        time.sleep(delay)
        # print(value)
        callback(publish_event, settings, value >= threshold)
        if stop_event.is_set():
            break