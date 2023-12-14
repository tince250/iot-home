import time
from queue import Empty
from locks import print_lock
# def get_user_input(input_queue, delay, stop_event):
#     while True:
#         try:
#             user_action = input("Enter action (B for sound): ")
#             if user_action.upper() == "B":
#                 input_queue.put("turn_sound_on")
#         except:
#             time.sleep(delay)
#             if stop_event.is_set():
#                 break

def run_buzzer_simulator(buzzer_queue, pitch, duration, buzzer_print_callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        try:
            action = buzzer_queue.get(timeout=1)
            if action == "turn_sound_on":
                buzzer_print_callback(publish_event, settings, status="ON")
                period = 1.0 / pitch
                delay = period / 2
                cycles = int(duration * pitch) 
                
                with print_lock:
                    for _ in range(cycles):
                        start = time.time()
                        while True:
                            if time.time()-start > delay:
                                break
                        # print("\n")
                        time.sleep(delay)
                        if stop_event.is_set():
                            break
                # with print_lock:
                buzzer_print_callback(publish_event, settings, status="OFF")
        except Empty:
            pass