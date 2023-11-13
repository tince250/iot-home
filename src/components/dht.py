from simulators.dht import run_dht_simulator
import threading
import time
from locks import print_lock

def dht_callback(humidity, temperature, code="DHTLIB_OK", sensor_name = ""):
    t = time.localtime()
    with print_lock:
        print("="*10, end=" ")
        print(sensor_name, end=" ")
        print("="*10)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C\n")


def run_dht(settings, threads, stop_event):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:    
            print(f"Starting {sensor_name} simulator")
        dht1_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, sensor_name, stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        with print_lock: 
            print(f"{sensor_name} simulator started")
    else:
        from sensors.dht import run_dht_loop, DHT
        with print_lock:    
            print(f"Starting {sensor_name} loop")
        dht = DHT(settings['pin'], sensor_name)
        dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event))
        dht1_thread.start()
        threads.append(dht1_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")
