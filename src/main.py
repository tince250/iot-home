import threading
from components.button import run_button
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        # dht1_settings = settings['DHT1']
        # run_dht(dht1_settings, threads, stop_event)
        button_settings = settings['button']
        run_button(button_settings, threads, stop_event)
        # uds1_settings = settings["UDS1"]
        # run_uds("UDS1", uds1_settings, threads, stop_event)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()
