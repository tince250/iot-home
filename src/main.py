import threading
from components.pir import run_pir
from components.button import run_button
from components.buzzer import run_buzzer
from settings import load_settings
from components.dht import run_dht
from components.uds import run_uds
from components.dl import run_dl
from components.ms import run_ms
import time
from queue import Queue
from locks import print_lock

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

def user_input_thread(queues_dict, stop_event):
    led_queue = queues_dict["door_light_queue"]
    buzzer_queue = queues_dict["buzzer_queue"]
    while True:
        try:
            user_action = input()
            if user_action.upper() == "X":
                led_queue.put("turn_on")
            elif user_action.upper() == "Y":
                led_queue.put("turn_off")
            elif user_action.upper() == "B":
                buzzer_queue.put("turn_sound_on")
        except:
            time.sleep(0.001)
            if stop_event.is_set():
                break

def run_user_input_thread(queues_dict : dict, stop_event, threads):
    input_thread = threading.Thread(target=user_input_thread, args=(queues_dict, stop_event))
    input_thread.start()
    threads.append(input_thread)

def get_queues_dict():
    queues_dict = {"door_light_queue" : Queue(), 
                   "buzzer_queue": Queue()}
    return queues_dict

def run_pi1(settings):
    rdht1_settings = settings['RDHT1']
    run_dht(rdht1_settings, threads, stop_event)

    rdht2_settings = settings['RDHT2']
    run_dht(rdht2_settings, threads, stop_event)

    # uds1_settings = settings["UDS1"]
    # run_uds(uds1_settings, threads, stop_event)
    
    # dpir1_settings = settings['DPIR1']
    # run_pir(dpir1_settings, threads, stop_event)
    # pir1_settings = settings['RPIR1']
    # run_pir(pir1_settings, threads, stop_event)
    # pir2_settings = settings['RPIR2']
    # run_pir(pir2_settings, threads, stop_event)

    # ds1_settings = settings['DS1']
    # run_button(ds1_settings, threads, stop_event)
    
    # dms_settings = settings["DMS"]
    # run_ms(dms_settings, threads, stop_event)
    
    # dl_settings = settings["DL"]
    # run_dl(dl_settings, threads, stop_event, queues_dict["door_light_queue"])
    
    # db_settings = settings['DB']
    # run_buzzer(db_settings, threads, stop_event, queues_dict["buzzer_queue"])


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
    queues_dict = get_queues_dict()

    try:
        run_pi1(settings)
        run_user_input_thread(queues_dict, stop_event, threads)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        with print_lock:
            print('Stopping app')
        for t in threads:
            stop_event.set()
        print("Stopped app")
