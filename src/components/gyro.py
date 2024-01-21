from simulators.gyro import run_gyro_simulator
import threading
import time
from locks import print_lock
import paho.mqtt.publish as publish
import json

gyro_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, gyro_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_gyro_batch = gyro_batch.copy()
            publish_data_counter = 0
            gyro_batch.clear()
        try:
            publish.multiple(local_gyro_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} gyroscope values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gyro_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def gyro_callback(angle, publish_event, gyro_settings, verbose=True):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(gyro_settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Rotation x: {angle['rotation_x']}")
            print(f"Rotation y: {angle['rotation_y']}")
            print(f"Rotation z: {angle['rotation_z']}")

    angle_payload = {
        "measurement": "Temperature",
        "simulated": gyro_settings['simulated'],
        "runs_on": gyro_settings["runs_on"],
        "name": gyro_settings["name"],
        "value": str(angle)[1:-1],
        "field": gyro_settings["influxdb_field"],
        "bucket": gyro_settings["influxdb_bucket"]
    }

    with counter_lock:
        gyro_batch.append(('topic/gyro/angles', json.dumps(angle_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_gyro(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:    
            print(f"Starting {sensor_name} simulator")
        gyro_thread = threading.Thread(target = run_gyro_simulator, args=(2, gyro_callback, stop_event, publish_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        with print_lock: 
            print(f"{sensor_name} simulator started")
    else:
        from sensors.gyro.gyro import run_gyro_loop, Gyroscope
        with print_lock:    
            print(f"Starting {sensor_name} loop")
        gyro = Gyroscope()
        gyro_thread = threading.Thread(target=run_gyro_loop, args=(gyro, 2, gyro_callback, stop_event, publish_event, settings))
        gyro_thread.start()
        threads.append(gyro_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")
