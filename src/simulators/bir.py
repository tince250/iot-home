import random
import time

def run_bir_simulator(delay, callback, stop_event, publish_event, settings, data_queue, change_color_event, bir_rgb_mappings):
    button_names = ["LEFT", "RIGHT", "UP", "DOWN",       
    "2", "3", "1", "OK", "4", "5", "6", "7", "8", "9", "*", "0", "#"] 
    while True:
        time.sleep(delay)
        clicked_button = button_names[random.randint(0, len(button_names)-1)]
        
        if clicked_button in bir_rgb_mappings.keys():
            data_queue.put(bir_rgb_mappings[clicked_button])
            change_color_event.set()
        
        callback(clicked_button, publish_event, settings)
        if stop_event.is_set():
            break