import threading
from locks import print_lock
import time
import threading
from locks import print_lock
import paho.mqtt.publish as publish
import json

button_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()

def publisher_task(event, button_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_button_batch = button_batch.copy()
            publish_data_counter = 0
            button_batch.clear()
        try:
            publish.multiple(local_button_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} button values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, button_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def button_callback(publish_event, settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"{settings['name']} is pressed!\n")

    press_payload = {
        "measurement": "button_press",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": "pressed",
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"]
    }

    with counter_lock:
        button_batch.append(('topic/button/press', json.dumps(press_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_button(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings["simulated"]:
        from simulators.button import run_button_simulator
        with print_lock:    
            print(f"Starting {sensor_name} simulator")
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_callback, stop_event, publish_event, settings))
        button_thread.start()
        threads.append(button_thread)
        with print_lock: 
            print(f"{sensor_name} simulator started")
    else:
        from sensors.button import Button, run_button_loop
        with print_lock: 
            print(f"Starting {sensor_name} loop")
        button = Button(settings['port'], sensor_name)
        button_thread = threading.Thread(target=run_button_loop, args=(button, stop_event, publish_event, settings))
        button_thread.start()
        threads.append(button_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")