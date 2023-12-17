from simulators.dht import run_dht_simulator
import threading
import time
from locks import print_lock
import paho.mqtt.publish as publish
import json

dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        try:
            publish.multiple(local_dht_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} dht values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def dht_callback(humidity, temperature, publish_event, dht_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(dht_settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Code: {code}")
            print(f"Humidity: {humidity}%")
            print(f"Temperature: {temperature}°C\n")

    temp_payload = {
        "measurement": "Temperature",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": temperature,
        "field": dht_settings["influxdb_field"],
        "bucket": dht_settings["influxdb_bucket"]
    }

    humidity_payload = {
        "measurement": "Humidity",
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": humidity,
        "field": dht_settings["influxdb_field"],
        "bucket": dht_settings["influxdb_bucket"]
    }

    with counter_lock:
        dht_batch.append(('topic/dht/temperature', json.dumps(temp_payload), 0, True))
        dht_batch.append(('topic/dht/humidity', json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:    
            print(f"Starting {sensor_name} simulator")
        dht1_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        with print_lock: 
            print(f"{sensor_name} simulator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        with print_lock:    
            print(f"Starting {sensor_name} loop")
        dht = DHT(settings['pin'], sensor_name)
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, publish_event, settings))
        dht1_thread.start()
        threads.append(dht1_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")
