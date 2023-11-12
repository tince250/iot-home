import threading

def button_callback():
    print("Button is clicked!")

def run_button(settings, threads, stop_event):
    if settings["simulated"]:
        from simulators.button import run_button_simulator
        print("Starting button simulator")
        button_thread = threading.Thread(target=run_button_simulator, args=(2, button_callback, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print("Button simulator started")
    else:
        from sensors.button import Button, run_button_loop
        print(f"Starting button loop")
        button = Button(settings['port_pin'])
        button_thread = threading.Thread(target=run_button_loop, args=(button, stop_event))
        button_thread.start()
        threads.append(button_thread)
        print(f"Button loop started")