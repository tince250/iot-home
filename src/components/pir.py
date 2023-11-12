import threading

from simulators.pir import run_pir_simulator

def motion_detected_callback(channel=None):
    print("You moved!")

def no_motion_callback(channel=None):
    print("You stopped moving!")

def run_pir(settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting pir simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, stop_event, motion_detected_callback, no_motion_callback))
        pir_thread.start()
        threads.append(pir_thread)
        print("Pir simulation started\n")
    else:
        from sensors.pir import PIR, run_pir_loop
        print(f"Starting PIR loop")
        pir = run_pir_loop(settings['pin'], motion_detected_callback, no_motion_callback)
        pir_thread = threading.Thread(target=run_pir_loop, args=(pir, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
        print(f"PIR loop started")