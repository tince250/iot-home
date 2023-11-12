import threading
import time
from simulators.dl import run_dl_dimulator
from locks import print_lock

def dl_callback(status):
    t = time.localtime()
    with print_lock:
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Status: {status}")


def run_dl(sensor_name, settings, threads, stop_event, input_queue):
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} sumilator")
        dl_thread = threading.Thread(target = run_dl_dimulator, args=(input_queue, 2, dl_callback, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        with print_lock:
            print(f"{sensor_name} sumilator started")
    else:
        from sensors.dl import run_dl_loop, DL
        with print_lock:
            print(f"Starting {sensor_name} loop")
        uds = DL(settings['trig'], settings["echo"])
        dl_thread = threading.Thread(target=run_dl_loop, args=(input_queue, uds, 2, dl_callback, stop_event))
        dl_thread.start()
        threads.append(dl_thread)
        with print_lock:
            print(f"{sensor_name} loop started")
