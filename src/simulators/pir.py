import random 
import time
from locks import print_lock

def generate_values(initial_value=0, threshold=0.6):
    value = initial_value
    while True:
        if value < 0:
            value = 0
        if value > 1:
            value = threshold
        value += random.uniform(-0.5, 0.5)
        yield value

def run_pir_simulator(delay, motion_detected_callback, no_motion_detected_callback, stop_event, publish_event, settings, threshold=0.6):
    previous_move = False
    for value in generate_values(threshold=threshold):
        time.sleep(delay)
        # print(value)
        is_move_detected = value > threshold
        if is_move_detected:
            if not previous_move:
                motion_detected_callback(publish_event, settings)
                previous_move = True
        else:
            if previous_move:
                no_motion_detected_callback(publish_event, settings)
                previous_move = False
        if stop_event.is_set():
                  break