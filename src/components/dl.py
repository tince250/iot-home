import threading
import time
from simulators.dl import run_dl_dimulator
from locks import print_lock
import paho.mqtt.publish as publish
import json

dl_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, dl_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dl_batch = dl_batch.copy()
            publish_data_counter = 0
            dl_batch.clear()
        try:
            publish.multiple(local_dl_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} door light values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dl_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dl_callback(status, publish_event, settings, verbose=False):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    formatted_time = time.strftime('%d.%m.%Y. %H:%M:%S', t)

    if verbose:
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Status: {status}\n")

    dl_payload = {
        "measurement": "door_light_toggled",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": status,
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"],
        "update_front": True,
        "datetime": formatted_time
    }

    with counter_lock:
        dl_batch.append(('topic/doorlight/toggle', json.dumps(dl_payload), 0, False))
        publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()


def run_dl(settings, threads, stop_event, input_queue, motion_detected_event=None):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        dl_thread = threading.Thread(target = run_dl_dimulator, args=(input_queue, 2, dl_callback, stop_event, publish_event, settings, motion_detected_event))
        dl_thread.start()
        threads.append(dl_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.dl import run_dl_loop, DL
        with print_lock:
            print(f"Starting {sensor_name} loop")
        dl = DL(settings['port'], sensor_name)
        dl_thread = threading.Thread(target=run_dl_loop, args=(input_queue, dl, 2, dl_callback, stop_event, publish_event, settings, motion_detected_event))
        dl_thread.start()
        threads.append(dl_thread)
        with print_lock:
            print(f"{sensor_name} loop started")
