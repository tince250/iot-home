import threading
import time
from simulators.uds import run_uds_simulator

def uds_callback(distance):
    t = time.localtime()
    print("="*20)
    print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
    if distance is not None:
        print(f'Distance: {distance} cm')
    else:
        print('Measurement timed out')

# TODO: Sta mislis nele ovako, da prosledimo sensor name ili da ceo settings prosledimo bez da fetchamo iz maina na osnovu naima nego to ovde
def run_uds(sensor_name, settings, threads, stop_event):
    if settings['simulated']:
        print(f"Starting {sensor_name} sumilator")
        uds1_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, stop_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        print(f"{sensor_name} sumilator started")
    else:
        from sensors.uds import run_uds_loop, UDS
        print(f"Starting {sensor_name} loop")
        uds = UDS(settings['trig'], settings["echo"])
        uds1_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, stop_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        print(f"{sensor_name} loop started")