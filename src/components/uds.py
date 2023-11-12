import threading
import time
from simulators.uds import run_uds_simulator
from locks import print_lock

def uds_callback(distance):
    t = time.localtime()

    with print_lock:
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        if distance is not None:
            print(f'Distance: {distance} cm')
        else:
            print('Measurement timed out')

def run_uds(sensor_name, settings, threads, stop_event):
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} sumilator")
        uds1_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, stop_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        with print_lock:
            print(f"{sensor_name} sumilator started")
    else:
        from sensors.uds import run_uds_loop, UDS
        with print_lock:
            print(f"Starting {sensor_name} loop")
        uds = UDS(settings['trig'], settings["echo"])
        uds1_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        with print_lock:
            print(f"{sensor_name} loop started")