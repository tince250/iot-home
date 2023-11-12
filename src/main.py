import threading
from components.button import run_button
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.dl import run_dl
import time
from queue import Queue
from locks import print_lock

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def user_input_thread(led_queue, stop_event):
    while True:
        try:
            user_action = input()
            if user_action.upper() == "X":
                led_queue.put("turn_on")
            elif user_action.upper() == "Y":
                led_queue.put("turn_off")
        except:
            time.sleep(0.001)
            if stop_event.is_set():
                break

def run_user_input_thread(door_light_queue, stop_event, threads):
    input_thread = threading.Thread(target=user_input_thread, args=(door_light_queue, stop_event))
    input_thread.start()
    threads.append(input_thread)

if __name__ == "__main__":
    with print_lock:
        print('Starting app')
        print("""To use actuators, type one of the options:
                'X' - turn on door light
                'Y' - turn off door light
                'B' - buzz """)
        
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    door_light_queue = Queue()

    try:
        # dht1_settings = settings['DHT1']
        # run_dht(dht1_settings, threads, stop_event)
#       button_settings = settings['button']
#       run_button(button_settings, threads, stop_event)
        dms_settings = settings["DMS"]
        run_ms("DMS", dms_settings, threads, stop_event)
        uds1_settings = settings["UDS1"]
        run_uds("UDS1", uds1_settings, threads, stop_event)
        dl_settings = settings["DL"]
        run_dl("DL", dl_settings, threads, stop_event, door_light_queue)

        run_user_input_thread(door_light_queue, stop_event, threads)
        
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        with print_lock:
            print('Stopping app')
        for t in threads:
            stop_event.set()
        print("Stopped app")
