import threading
import time
from simulators.uds import run_uds_simulator
from locks import print_lock
import paho.mqtt.publish as publish
import json

uds_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()

def publisher_task(event, uds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = uds_batch.copy()
            publish_data_counter = 0
            uds_batch.clear()
        try:
            publish.multiple(local_dht_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} uds values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, uds_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def uds_callback(distance, publish_event, settings, verbose=True):
    global publish_data_counter, publish_data_limit
    
    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings["name"], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            if distance is not None:
                print(f'Distance: {distance} cm\n')
            else:
                print('Measurement timed out\n')

    distance_payload = {
        "measurement": "Distance",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": distance,
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"],
        "update_front": False
    }

    with counter_lock:
        if publish_data_counter == publish_data_limit - 1:
            distance_payload["update_front"] = True
        uds_batch.append(('topic/uds/distance', json.dumps(distance_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()
    

def run_uds(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        uds1_thread = threading.Thread(target = run_uds_simulator, args=(2, uds_callback, settings, publish_event, stop_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.uds import run_uds_loop, UDS
        with print_lock:
            print(f"Starting {sensor_name} loop")
        uds = UDS(settings['trig'], settings["echo"], sensor_name)
        uds1_thread = threading.Thread(target=run_uds_loop, args=(uds, 2, uds_callback, settings, publish_event, stop_event))
        uds1_thread.start()
        threads.append(uds1_thread)
        with print_lock:
            print(f"{sensor_name} loop started")