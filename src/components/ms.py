import threading
import time
from simulators.ms import run_ms_simulator
from locks import print_lock

def ms_callback(pressed_key):
    t = time.localtime()
    with print_lock: 
        print("="*20)
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        if pressed_key is not None:
            print(f'Pressed key: {pressed_key}')
        else:
            print('No keys pressed')

def run_ms(sensor_name, settings, threads, stop_event):
    if settings['simulated']:
        with print_lock: 
            print(f"Starting {sensor_name} sumilator")
        ms_thread = threading.Thread(target = run_ms_simulator, args=(2, ms_callback, stop_event))
        ms_thread.start()
        threads.append(ms_thread)
        with print_lock: 
            print(f"{sensor_name} sumilator started")
    else:
        from sensors.ms import run_ms_loop, MS
        with print_lock: 
            print(f"Starting {sensor_name} loop")
        ms = MS(R1=settings["R1"], R2=settings["R2"],  R3=settings["R3"],  R4=settings["R4"], C1=settings["C1"], C2=settings["C2"], C3=settings["C3"], C4=settings["C4"])
        ms_thread = threading.Thread(target=run_ms_loop, args=(ms, 2, ms_callback, stop_event))
        ms_thread.start()
        threads.append(ms_thread)
        with print_lock: 
            print(f"{sensor_name} loop started")