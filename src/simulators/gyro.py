import time
import random

def generate_values():
    while True:
        rotation_x = round(random.uniform(-10.0, 10.0), 2) 
        rotation_y = round(random.uniform(-10.0, 10.0), 2)  
        rotation_z = round(random.uniform(-10.0, 10.0), 2) 

        yield {
            "rotation_x": rotation_x,
            "rotation_y": rotation_y,
            "rotation_z": rotation_z
        }

        time.sleep(0.1)

def run_gyro_simulator(delay, callback, stop_event, publish_event, settings):
        for angles in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(angles, publish_event, settings, True)
            if stop_event.is_set():
                  break