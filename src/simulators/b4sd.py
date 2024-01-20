import random
import time

def run_b4sd_simulator(delay, callback, stop_event, settings):
   # print(settings["digits"][0])
    #print(type(settings["digits"][0]))
    while True:
        current_time = time.ctime()[11:13]+time.ctime()[14:16]
        current_time_s = str(current_time[:2])+":"+str(current_time[2:])
        callback(settings, current_time_s)
        time.sleep(delay)
        if stop_event.is_set():
            break