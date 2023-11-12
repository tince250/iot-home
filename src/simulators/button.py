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

def run_button_simulator(delay, callback, sensor_name, stop_event, threshold=0.6):
    for value in generate_values(threshold=threshold):
        time.sleep(delay)
        # print(value)
        if value >= threshold:
            callback(sensor_name)
        if stop_event.is_set():
            break