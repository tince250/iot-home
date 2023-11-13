import threading
import time
from locks import print_lock
from simulators.pir import run_pir_simulator

def motion_detected_callback(sensor_name=""):
    t = time.localtime()
    with print_lock:
        print("="*10, end=" ")
        print(sensor_name, end=" ")
        print("="*10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("You moved!\n")

def no_motion_detected_callback(sensor_name=""):
    t = time.localtime()
    with print_lock:
        print("="*10, end=" ")
        print(sensor_name, end=" ")
        print("="*10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print("You stopped moving!\n")

def run_pir(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings["simulated"]:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, sensor_name,  motion_detected_callback, no_motion_detected_callback, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.pir import PIR, run_pir_loop
        with print_lock:
            print(f"Starting {sensor_name} loop")
        # pir = run_pir_loop(settings['pin'], motion_detected_callback, no_motion_callback)
        pir = PIR(settings['port'], motion_detected_callback, no_motion_detected_callback, sensor_name)
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
        with print_lock:
            print(f"{sensor_name} loop started")