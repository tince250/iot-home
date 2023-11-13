import threading
from locks import print_lock
import time

def button_callback(sensor_name=""):
    t = time.localtime()
    with print_lock:
        print("="*10, end=" ")
        print(sensor_name, end=" ")
        print("="*10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"{sensor_name} is clicked!\n")

def run_button(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings["simulated"]:
        from simulators.button import run_button_simulator
        with print_lock:    
            print(f"Starting {sensor_name} simulator")
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_callback, sensor_name, stop_event))
        button_thread.start()
        threads.append(button_thread)
        with print_lock: 
            print(f"{sensor_name} simulator started")
    else:
        from sensors.button import Button, run_button_loop
        with print_lock: 
            print(f"Starting {sensor_name} loop")
        button = Button(settings['port'], sensor_name)
        button_thread = threading.Thread(target=run_button_loop, args=(button, stop_event))
        button_thread.start()
        threads.append(button_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")