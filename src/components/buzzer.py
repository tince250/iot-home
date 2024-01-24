import threading
from queue import Queue
from simulators.buzzer import run_buzzer_simulator
import time
from locks import print_lock
import threading
import time
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
from threading import Event
buzzer_batch = []
publish_data_counter = 0
publish_data_limit = 1
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

def buzzer_print_callback(publish_event, settings, status="ON", verbose=True):
    global publish_data_counter, publish_data_limit

    t = time.localtime()
    formatted_time = time.strftime('%d.%m.%Y. %H:%M:%S', t)

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
        "bucket": settings["influxdb_bucket"],
        "datetime": formatted_time
    }

    with counter_lock:
        if publish_data_counter == publish_data_limit - 1:
            sound_payload["update_front"] = True
        buzzer_batch.append(('topic/buzzer/sound', json.dumps(sound_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def on_connect(client: mqtt.Client, userdata: any, flags, result_code):
    print("Connected with result code "+str(result_code))
    client.subscribe("topic/alarm/buzzer/on")
    client.subscribe("topic/alarm/buzzer/off")

def on_receive(msg, alarm_on_event):
    # print(msg.topic)
    if msg.topic == "topic/alarm/buzzer/on":
        alarm_on_event.set()
    elif msg.topic == "topic/alarm/buzzer/off":
        #data = json.loads(msg.payload.decode('utf-8'))
        alarm_on_event.clear()

def run_buzzer(settings, threads, stop_event, alarm_on_event, alarm_clock_queue=None, alarm_clock_on_event=None, alarm_clock_off_event=None):
    delay, pitch, duration = 1, 1000, 0.1

    sensor_name = settings["name"]
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: on_receive(msg, alarm_on_event)
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
    
    if settings["simulated"]:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(alarm_clock_queue, pitch, duration,
                                                                            alarm_clock_queue, alarm_on_event,
                                                                              alarm_clock_on_event, alarm_clock_off_event,
                                                                             buzzer_print_callback, stop_event,
                                                                            publish_event, settings))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.buzzer import Buzzer, run_buzzer_loop
        with print_lock:
            print(f"Starting {sensor_name} loop")
        buzzer = Buzzer(settings['pin'], sensor_name)
        buzzer_queue = 0
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(alarm_clock_queue, buzzer, pitch, duration,
                                                                        delay, alarm_on_event, alarm_clock_on_event, alarm_clock_off_event,
                                                                        buzzer_print_callback, stop_event,
                                                                        publish_event, settings))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        with print_lock:
            print(f"{sensor_name} loop started")