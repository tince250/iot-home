
from queue import Empty
import time
import random

def generate_values(data_queue, initial_temp = 25, initial_humidity=20):
    temperature = initial_temp
    humidity = initial_humidity
    temperature = temperature + random.randint(-1, 1)
    humidity = humidity + random.randint(-1, 1)
    if humidity < 0:
        humidity = 0
    if humidity > 100:
        humidity = 100

    return temperature, humidity

def run_lcd_simulator(data_queue, delay, callback, stop_event, settings):
    #TODO: implementiraj da uzme od DHT simulatora
    while not stop_event.is_set():
        try:
            temperature, humidity = generate_values(data_queue)
            callback(temperature, humidity, settings, True)
        except Empty:
            pass
        time.sleep(delay)
