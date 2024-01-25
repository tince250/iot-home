import random
import time

def generate_values(delay, initial_value=0):
    value = initial_value
    previous_value = None
    while True:
        time.sleep(delay)
        value = random.randint(0,1) == 1
        if value != previous_value:
            previous_value = value
            yield value
        else:
            continue
        # if value < 0:
        #     value = 0
        # if value > 1:
        #     value = threshold
        # value += random.uniform(-0.5, 0.5)
        # yield value

def run_button_simulator(delay, callback, stop_event, publish_event, settings, threshold=0.6):
    # for value in generate_values(delay=1):
    #     # print(value)
    #     callback(publish_event, settings, value == 1)
    #     if stop_event.is_set():
    #         break

    callback(publish_event, settings, False)

    while True:
        if stop_event.is_set():
            break