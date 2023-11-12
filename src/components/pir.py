import threading

from simulators.pir import run_pir_simulator

def run_pir(settings, threads, stop_event):
    if settings["simulated"]:
        print("Starting pir simulator")
        pir_thread = threading.Thread(target=run_pir_simulator, args=(2, stop_event))
        pir_thread.start()
        threads.append(pir_thread)
        print("Pir simulation started\n")
    else:
        return