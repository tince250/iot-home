import threading
import time
# from simulators.lcd import run_lcd_simulator
from locks import print_lock
import paho.mqtt.publish as publish
import json

lcd_batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()

def publisher_task(event, lcd_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_lcd_batch = lcd_batch.copy()
            publish_data_counter = 0
            lcd_batch.clear()
        try:
            publish.multiple(local_lcd_batch, hostname="localhost", port=1883)
            print(f'Published {publish_data_limit} lcd values')
        except:
            print("greska")
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, lcd_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def lcd_callback(text, publish_event, settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Text: {text}\n")

    lcd_payload = {
        "measurement": "lcd_displayed",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": text,
        "field": settings["influxdb_field"],
        "bucket": settings["influxdb_bucket"]
    }

    with counter_lock:
        lcd_batch.append(('topic/lcd/text', json.dumps(lcd_payload), 0, False))
        publish_data_counter += 1

        if publish_data_counter >= publish_data_limit:
            publish_event.set()


def run_lcd(settings, threads, stop_event, input_queue):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        # lcd_thread = threading.Thread(target = run_lcd_simulator, args=(input_queue, 2, lcd_callback, stop_event, publish_event, settings))
        # lcd_thread.start()
        # threads.append(lcd_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.dl import run_lcd_loop, DL
        with print_lock:
            print(f"Starting {sensor_name} loop")
        dl = DL(settings['port'], sensor_name)
        lcd_thread = threading.Thread(target=run_lcd_loop, args=(input_queue, dl, 2, lcd_callback, stop_event, publish_event, settings))
        lcd_thread.start()
        threads.append(lcd_thread)
        with print_lock:
            print(f"{sensor_name} loop started")
