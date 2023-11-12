import threading
from locks import print_lock

def button_callback():
    with print_lock:
        print("Button is clicked!")

def run_button(settings, threads, stop_event):
    if settings["simulated"]:
        from simulators.button import run_button_simulator
        with print_lock:    
            print("Starting button simulator")
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_callback, stop_event))
        button_thread.start()
        threads.append(button_thread)
        with print_lock: 
            print("Button simulator started")
    else:
        from sensors.button import Button, run_button_loop
        with print_lock: 
            print(f"Starting button loop")
        button = Button(settings['port_pin'])
        button_thread = threading.Thread(target=run_button_loop, args=(button, stop_event))
        button_thread.start()
        threads.append(button_thread)
        with print_lock: 
            print(f"Button loop started")