import threading
import time
from locks import print_lock
import paho.mqtt.publish as publish
import json
from simulators.pir import run_pir_simulator

pir_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, pir_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = pir_batch.copy()
            publish_data_counter = 0
            pir_batch.clear()
        try:
            publish.multiple(local_pir_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} pir values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def motion_detected_callback(publish_event, settings,verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings["name"], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print("You moved!\n")

    move_payload = {
        "measurement": "pir_move",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": "moved",
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"]
    }

    with counter_lock:
        if publish_data_counter == publish_data_limit - 1:
            move_payload["update_front"] = True
        pir_batch.append(('topic/pir/move', json.dumps(move_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def no_motion_detected_callback(publish_event, settings,verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings["name"], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print("You stopped moving!\n")

    move_payload = {
        "measurement": "pir_move",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": "stopped",
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"],
    }

    with counter_lock:
        if publish_data_counter == publish_data_limit - 1:
            move_payload["update_front"] = True
        pir_batch.append(('topic/pir/move', json.dumps(move_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_pir(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings["simulated"]:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2,  motion_detected_callback, no_motion_detected_callback, stop_event,
                                                                      publish_event, settings))
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