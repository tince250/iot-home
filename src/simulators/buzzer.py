import time

def run_buzzer_simulator(pitch, duration, stop_event):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch) 
    for _ in range(cycles):
        start = time.time()
        while True:
            if time.time()-start > delay:
                break
            print("A", end="")
        print("\n")
        time.sleep(delay)
        if stop_event.is_set():
            break
    print("Sound off")