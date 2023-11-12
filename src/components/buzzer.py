import threading
from queue import Queue
from simulators.buzzer import get_user_input, run_buzzer_simulator

def run_buzzer(settings, threads, stop_event):
    if settings["simulated"]:
        input_queue = Queue()
        delay = 1
        print("Starting buzzer on input thread")
        buzzer_on_input_thread = threading.Thread(target=get_user_input, args=(input_queue, delay, stop_event))
        buzzer_on_input_thread.start()
        print("Buzzer on input thread started")

        pitch = 1000
        duration = 0.1
        print("Starting buzzer simulator")
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(input_queue, pitch, duration, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("Buzzer simulator started")
    else:
        return