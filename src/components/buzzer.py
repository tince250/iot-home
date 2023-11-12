import threading
from queue import Queue
from simulators.buzzer import get_user_input, run_buzzer_simulator

def run_buzzer(settings, threads, stop_event):
    delay, pitch, duration = 1, 1000, 0.1
    
    if settings["simulated"]:
        input_queue = Queue()
        
        print("Starting buzzer on input thread")
        buzzer_on_input_thread = threading.Thread(target=get_user_input, args=(input_queue, delay, stop_event))
        buzzer_on_input_thread.start()
        print("Buzzer on input thread started")

        
        print("Starting buzzer simulator")
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(input_queue, pitch, duration, stop_event))
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