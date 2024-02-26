import threading
import time
from simulators.lcd import run_lcd_simulator
from locks import print_lock
import paho.mqtt.publish as publish
import json
from queue import Queue


def lcd_callback(temperature, humidity, settings, verbose=False):

    if verbose:
        t = time.localtime()
        with print_lock:
            print("="*10, end=" ")
            print(settings['name'], end=" ")
            print("="*10)
            print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
            print(f"Received temperature: {temperature}\n")
            print(f"Received humidity: {humidity}\n")

def run_lcd(settings, threads, stop_event, display_values_event, data_queue):
    sensor_name = settings["name"]
    if settings['simulated']:
        with print_lock:
            print(f"Starting {sensor_name} simulator")
        lcd_thread = threading.Thread(target = run_lcd_simulator, args=(2, lcd_callback, stop_event, settings, display_values_event, data_queue))
        lcd_thread.start()
        threads.append(lcd_thread)
        with print_lock:
            print(f"{sensor_name} simulator started")
    else:
        from sensors.lcd.LCD1602 import run_lcd_loop, LCD
        with print_lock:
            print(f"Starting {sensor_name} loop")
        lcd = LCD()
        lcd_thread = threading.Thread(target=run_lcd_loop, args=(lcd, 2, lcd_callback, stop_event, settings, display_values_event, data_queue))
        lcd_thread.start()
        threads.append(lcd_thread)
        with print_lock:
            print(f"{sensor_name} loop started")
