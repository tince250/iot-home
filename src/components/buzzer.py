import threading
from queue import Queue
from simulators.buzzer import run_buzzer_simulator
import time
from locks import print_lock

def buzzer_print_callback(status="ON", sensor_name=""):
    t = time.localtime()
    with print_lock:
        print("="*10, end=" ")
        print(sensor_name, end=" ")
        print("="*10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Sound: {status}\n")


def run_buzzer(settings, threads, stop_event, buzzer_queue):
    delay, pitch, duration = 1, 1000, 0.1
    sensor_name = settings["name"]
    
    if settings["simulated"]:
        print(f"Starting {sensor_name} simulator")
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(buzzer_queue, pitch, duration, sensor_name, buzzer_print_callback, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print(f"{sensor_name} simulator started")
    else:
        from sensors.buzzer import Buzzer, run_buzzer_loop
        print(f"Starting {sensor_name} loop")
        buzzer = Buzzer(settings['pin'], sensor_name)
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer_queue, buzzer, pitch, duration, delay, buzzer_print_callback, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print(f"{sensor_name} loop started")