import time
import random

def generate_values():
      while True:
            distance = random.randrange(0, 50)
            if distance > 40:
                distance = None
            yield distance

      

def run_uds_simulator(delay, callback, settings, publish_event, stop_event):
        for dist in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(dist, publish_event, settings)
            if stop_event.is_set():
                  break