import random
import time

# second idea because of rising and falling:
# def generate_values(initial_value=0):
#     while True:
#         initial_value += random.randint(-1, 1)
#         if initial_value < 0:
#             initial_value = 0
#         if initial_value > 1:
#             initial_value = 1
#         yield initial_value

# def run_pir_simulator(delay, callback, stop_event, threshold=0.8):
#     previous_move = False
#     for value in generate_values():
#         time.sleep(2)
#         if initial_value >= threshold:
            # callback()
        # initial_value = random.random()
        # if stop_event.is_set():
        #     break

def run_button_simulator(delay, callback, stop_event, threshold=0.8):
    initial_value = 0
    while True:
        time.sleep(delay)
        if initial_value >= threshold:
            callback()
        initial_value = random.random()
        if stop_event.is_set():
            break