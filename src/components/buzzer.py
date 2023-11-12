import threading
from queue import Queue
from simulators.buzzer import run_buzzer_simulator

def run_buzzer(settings, threads, stop_event, buzzer_queue):
    delay, pitch, duration = 1, 1000, 0.1
    
    if settings["simulated"]:
        print("Starting buzzer simulator")
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(buzzer_queue, pitch, duration, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("Buzzer simulator started")
    else:
        from sensors.buzzer import Buzzer, run_buzzer_loop
        print(f"Starting buzzer loop")
        buzzer = Buzzer(settings['pin'])
        buzzer_thread = threading.Thread(target=run_buzzer_loop, args=(buzzer, pitch, duration, delay, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print(f"Buzzer loop started")