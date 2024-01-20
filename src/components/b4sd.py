import threading
from locks import print_lock
import time
import threading
from locks import print_lock
import paho.mqtt.publish as publish
import json

def b4sd_callback(settings, current_time, verbose=True):
    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"{settings['name']}: {current_time}\n")


def run_b4sd(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings["simulated"]:
        from simulators.b4sd import run_b4sd_simulator
        with print_lock:    
            print(f"Starting {sensor_name} simulator")
        b4sd_thread = threading.Thread(target=run_b4sd_simulator, args=(5, b4sd_callback, stop_event, settings))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        with print_lock: 
            print(f"{sensor_name} simulator started")
    else:
        from sensors.b4sd import B4SD, run_b4sd_loop
        with print_lock: 
            print(f"Starting {sensor_name} loop")
        b4sd = B4SD(settings["digits"], settings["segments"])
        b4sd_thread = threading.Thread(target=run_b4sd_loop, args=(b4sd, b4sd_callback, stop_event, settings))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")