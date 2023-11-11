from simulators.dht import run_dht_simulator
import threading
import time

def run_button_simulator(delay, callback, stop_event, threshold=0.8):
    initial_value = 0
    while True:
        time.sleep(delay)
        if initial_value >= threshold:
            callback()
        initial_value = random.random()
        if stop_event.is_set():
            break
