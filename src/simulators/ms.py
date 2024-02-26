import time
import random

keypad_layout = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# def generate_values():
#       while True:
#             pressed_key = None
            
#             is_key_pressed = random.choice([True, False])
#             if is_key_pressed:
#                 row_index = random.randint(0, 3)
#                 col_index = random.randint(0, 3)
#                 pressed_key = keypad_layout[row_index][col_index]
                
#             yield pressed_key

def generate_values():
      for elem in ["*", "1", "2", "3", "4", "#"]:
            yield elem 
            
def run_ms_simulator(delay, callback, stop_event, settings, publish_event):
        for pressed_key in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            if pressed_key:
                callback(pressed_key, settings, publish_event)
            if stop_event.is_set():
                  break