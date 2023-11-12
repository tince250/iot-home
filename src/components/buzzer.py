import threading
from simulators.buzzer import run_buzzer_simulator

def run_buzzer(settings, threads, stop_event):
    if settings["simulated"]:
        pitch = 1000
        duration = 0.1
        print("Starting buzzer simulator")
        buzzer_thread = threading.Thread(target=run_buzzer_simulator, args=(pitch, duration, stop_event))
        buzzer_thread.start()
        threads.append(buzzer_thread)
        print("Buzzer simulator started")
    else:
        return