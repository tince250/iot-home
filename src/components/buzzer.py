import threading
from queue import Queue
from simulators.buzzer import run_buzzer_simulator
import time
from locks import print_lock
import threading
import time
import paho.mqtt.publish as publish
import json

buzzer_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()

def publisher_task(event, buzzer_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_buzzer_batch = buzzer_batch.copy()
            publish_data_counter = 0
            buzzer_batch.clear()
        try:
            publish.multiple(local_buzzer_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} buzzer values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, buzzer_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def buzzer_print_callback(publish_event, settings, status="ON", verbose=False):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    if verbose:
        with print_lock:
            print("="*10, end=" ")
            print(settings["name"], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Sound: {status}\n")
    
    sound_payload = {
        "measurement": "buzzer_sound",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": status,
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"]
    }

    with counter_lock:
        buzzer_batch.append(('topic/buzzer/sound', json.dumps(sound_payload), 0, True))
        publish_data_counter += 1
        print(publish_data_counter)

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_buzzer(settings, threads, stop_event, buzzer_queue):
    delay, pitch, duration = 1, 1000, 0.1
    sensor_name = settings["name"]
    
    if settings["simulated"]:
        print(f"Starting {sensor_name} simulator")
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(buzzer_queue, pitch, duration,
                                                                             buzzer_print_callback, stop_event,
                                                                            publish_event, settings))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print(f"{sensor_name} simulator started")
    else:
        from sensors.buzzer import Buzzer, run_buzzer_loop
        print(f"Starting {sensor_name} loop")
        buzzer = Buzzer(settings['pin'], sensor_name)
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer_queue, buzzer, pitch, duration,
                                                                        delay, buzzer_print_callback, stop_event,
                                                                        publish_event, settings))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print(f"{sensor_name} loop started")