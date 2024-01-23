import threading
from locks import print_lock
import time
import threading
from locks import print_lock
import paho.mqtt.publish as publish
import json
import paho.mqtt.client as mqtt
from queue import Queue
from threading import Event

def user_input_thread(mqtt_client, alarm_on_event, alarm_off_event, stop_event):
    alarm_on_set = False
    while True:
        if alarm_on_event.is_set():
            if not alarm_on_set:
                alarm_on_set = True
                data = {
                    "action": "on"
                }
                mqtt_client.publish("topic/clock-alarm/server", json.dumps(data))
        if alarm_off_event.is_set():
            if alarm_on_set:
                alarm_on_set = False
                data = {
                    "action": "off"
                }
                mqtt_client.publish("topic/clock-alarm/server", json.dumps(data))
        time.sleep(1)
        if stop_event.is_set():
            break

def run_user_input_thread(mqtt_client, alarm_on_event, alarm_off_event, stop_event, threads):
    input_thread = threading.Thread(target=user_input_thread, args=(mqtt_client, alarm_on_event, alarm_off_event, stop_event))
    input_thread.start()
    threads.append(input_thread)

def on_connect(client: mqtt.Client, userdata: any, flags, result_code):
    print("Connected with result code "+str(result_code))
    client.subscribe("topic/clock-alarm/device/on")
    client.subscribe("topic/clock-alarm/device/off")

def on_receive(msg, b4sd_queue, alarm_on_event, alarm_off_event):
    print(msg.topic)
    if msg.topic == "topic/clock-alarm/device/off":
        alarm_off_event.set()
    else:
        data = json.loads(msg.payload.decode('utf-8'))
        alarm_off_event.clear()
        b4sd_queue.put(data)
        print(data)
    # try:
    #     if data["action"] and data["action"] == "off":
    #         alarm_off_event.set()
    # except:

def b4sd_callback(settings, current_time, verbose=True):
    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"{settings['name']}: {current_time}\n")


def run_b4sd(settings, threads, stop_event):
    sensor_name = settings["name"]
    b4sd_queue = Queue()
    alarm_on_event = Event()
    alarm_off_event = Event()

    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = lambda client, userdata, msg: on_receive(msg, b4sd_queue, alarm_on_event, alarm_off_event)
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.loop_start()
    

    run_user_input_thread(mqtt_client, alarm_on_event, alarm_off_event, stop_event, threads)

    if settings["simulated"]:
        from simulators.b4sd import run_b4sd_simulator
        with print_lock:    
            print(f"Starting {sensor_name} simulator")
        b4sd_thread = threading.Thread(target=run_b4sd_simulator, args=(5, b4sd_callback, b4sd_queue, alarm_on_event, alarm_off_event, stop_event, settings))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        with print_lock: 
            print(f"{sensor_name} simulator started")
    else:
        from sensors.b4sd import B4SD, run_b4sd_loop
        with print_lock: 
            print(f"Starting {sensor_name} loop")
        b4sd = B4SD(settings["digits"], settings["segments"])
        b4sd_thread = threading.Thread(target=run_b4sd_loop, args=(b4sd, b4sd_callback, stop_event, settings))
        b4sd_thread.start()
        threads.append(b4sd_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")