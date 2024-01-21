import threading
import time
from simulators.rgb import run_rgb_simulator
from locks import print_lock
import paho.mqtt.publish as publish
import json

rgb_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()

def publisher_task(event, rgb_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = rgb_batch.copy()
            publish_data_counter = 0
            rgb_batch.clear()
        try:
            publish.multiple(local_rgb_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} rgb diode values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def rgb_callback(status, publish_event, settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Status: {status}\n")

    rgb_payload = {
        "measurement": "door_light_toggled",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": status,
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"]
    }

    with counter_lock:
        rgb_batch.append(('topic/rgbdiode/status', json.dumps(rgb_payload), 0, False))
        publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()


def run_rgb(settings, threads, stop_event, input_queue):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        rgb_thread = threading.Thread(target = run_rgb_simulator, args=(input_queue, 2, rgb_callback, stop_event, publish_event, settings))
        rgb_thread.start()
        threads.append(rgb_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.rgb import run_rgb_loop, RGBdiode
        with print_lock:
            print(f"Starting {sensor_name} loop")
        dl = RGBdiode(RED = settings['RED'], GREEN = settings['GREEN'], BLUE = settings['BLUE'])
        rgb_thread = threading.Thread(target=run_rgb_loop, args=(input_queue, dl, 2, rgb_callback, stop_event, publish_event, settings))
        rgb_thread.start()
        threads.append(rgb_thread)
        with print_lock:
            print(f"{sensor_name} loop started")
