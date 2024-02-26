import threading
import time
from simulators.ms import run_ms_simulator
from locks import print_lock
import paho.mqtt.publish as publish
import json
import traceback

ms_batch = []
publish_data_counter = 0
publish_data_limit = 6
code_sequence = ""
counter_lock = threading.Lock()

def publisher_task(event, ms_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = ms_batch.copy()
            publish_data_counter = 0
            ms_batch.clear()
        try:
            # publish.multiple(local_dht_batch, hostname="10.1.121.69", port=1883)
            publish.multiple(local_dht_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} ms values')
        except:
            traceback.print_exc() 
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ms_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def ms_callback(pressed_key, settings, publish_event, verbose=False):
    global publish_data_counter, publish_data_limit, code_sequence

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings["name"], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            if pressed_key is not None:
                print(f'Pressed key: {pressed_key}\n')
            else:
                print('No keys pressed\n')

    ms_payload = {
        "measurement": "key_pressed",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": pressed_key,
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"]
    }

    with counter_lock:
        ms_batch.append(('topic/ms/key-pressed', json.dumps(ms_payload), 0, True))
        publish_data_counter += 1

    if pressed_key == "*":
        code_sequence = ""
        code_sequence += pressed_key
    elif pressed_key != "#" and len(code_sequence) > 0 and len(code_sequence) < 5:
        code_sequence += pressed_key
    elif pressed_key == "#" and len(code_sequence) == 5:
        publish.single('topic/ms/code', payload=json.dumps({"code": code_sequence[1:]}), qos=0, retain=True, hostname="localhost", port=1883)
        print("published code seqeunce: " + code_sequence)
        code_sequence = ""

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

    

def run_ms(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock: 
            print(f"Starting {sensor_name} sumilator")
        ms_thread = threading.Thread(target = run_ms_simulator, args=(2, ms_callback, stop_event, settings, publish_event))
        ms_thread.start()
        threads.append(ms_thread)
        with print_lock: 
            print(f"{sensor_name} sumilator started")
    else:
        from sensors.ms import run_ms_loop, MS
        with print_lock: 
            print(f"Starting {sensor_name} loop")
        ms = MS(R1=settings["R1"], R2=settings["R2"],  R3=settings["R3"],  R4=settings["R4"], C1=settings["C1"], C2=settings["C2"], C3=settings["C3"], C4=settings["C4"], sensor_name=sensor_name)
        ms_thread = threading.Thread(target=run_ms_loop, args=(ms, 0.2, ms_callback, stop_event, settings, publish_event))
        ms_thread.start()
        threads.append(ms_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")