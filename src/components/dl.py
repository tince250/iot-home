import threading
import time
from simulators.dl import run_dl_dimulator
from locks import print_lock

def dl_callback(status, sensor_name = ""):
    t = time.localtime()
    with print_lock:
        print("="*10, end=" ")
        print(sensor_name, end=" ")
        print("="*10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Status: {status}\n")


def run_dl(settings, threads, stop_event, input_queue):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        dl_thread = threading.Thread(target = run_dl_dimulator, args=(input_queue, 2, dl_callback, sensor_name, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.dl import run_dl_loop, DL
        with print_lock:
            print(f"Starting {sensor_name} loop")
        dl = DL(settings['port'], sensor_name)
        dl_thread = threading.Thread(target=run_dl_loop, args=(input_queue, dl, 2, dl_callback, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        with print_lock:
            print(f"{sensor_name} loop started")
