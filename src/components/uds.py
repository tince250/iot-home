import threading
import time
from simulators.uds import run_uds_simulator
from locks import print_lock

def uds_callback(distance, sensor_name = ""):
    t = time.localtime()
    with print_lock:
        print("="*10, end=" ")
        print(sensor_name, end=" ")
        print("="*10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        if distance is not None:
            print(f'Distance: {distance} cm\n')
        else:
            print('Measurement timed out\n')

def run_uds(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        uds1_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, sensor_name, stop_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.uds import run_uds_loop, UDS
        with print_lock:
            print(f"Starting {sensor_name} loop")
        uds = UDS(settings['trig'], settings["echo"], sensor_name)
        uds1_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        with print_lock:
            print(f"{sensor_name} loop started")