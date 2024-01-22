import threading
from locks import print_lock
import time
import threading
from locks import print_lock
import paho.mqtt.publish as publish
import json

bir_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()

def publisher_task(event, bir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_bir_batch = bir_batch.copy()
            publish_data_counter = 0
            bir_batch.clear()
        try:
            publish.multiple(local_bir_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} bir values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, bir_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def bir_callback(clicked_button, publish_event, settings, verbose=True):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Clicked button: {clicked_button}\n")

    press_payload = {
        "measurement": "bir_button",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": clicked_button,
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"]
    }

    with counter_lock:
        bir_batch.append(('topic/bir/button', json.dumps(press_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_bir(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings["simulated"]:
        from simulators.bir import run_bir_simulator
        with print_lock:    
            print(f"Starting {sensor_name} simulator")
        bir_thread = threading.Thread(target=run_bir_simulator, args=(2, bir_callback, stop_event, publish_event, settings))
        bir_thread.start()
        threads.append(bir_thread)
        with print_lock: 
            print(f"{sensor_name} simulator started")
    else:
        from sensors.bir import BIR, run_bir_loop
        with print_lock: 
            print(f"Starting {sensor_name} loop")
        bir = BIR(settings['pin'], sensor_name)
        bir_thread = threading.Thread(target=run_bir_loop, args=(bir, bir_callback, stop_event, publish_event, settings))
        bir_thread.start()
        threads.append(bir_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")