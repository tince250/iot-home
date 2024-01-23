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

def run_buzzer_simulator(alarm_clock_queue, pitch, duration,
                         ass, alarm_clock_on_event, alarm_clock_off_event, 
                         buzzer_print_callback, stop_event, publish_event, settings):
    current_clock_alarm = None
    called_callback = False
    while True:
        if stop_event.is_set():
            return
        if alarm_clock_on_event:
            while not alarm_clock_off_event.is_set():
                try:
                    current_clock_alarm = alarm_clock_queue.get(timeout=1)
                except Empty:
                    pass
                if current_clock_alarm and is_after_current_time(current_clock_alarm['date'], current_clock_alarm['time']):
                    if not alarm_clock_on_event.is_set():
                        alarm_clock_on_event.set()
                    if not called_callback:
                        buzzer_print_callback(publish_event, settings, status="ON")
                        called_callback = True
                    delay = 1.0 / (pitch*2)
                    time.sleep(delay)
                    # period = 1.0 / pitch
                    # delay = period / 2
                    # cycles = int(duration * pitch) 
                    
                    # with print_lock:
                    #     for _ in range(cycles):
                    #         start = time.time()
                    #         while True:
                    #             if time.time()-start > delay:
                    #                 break
                    #         # print("\n")
                    #         time.sleep(delay)
                # with print_lock:
            if current_clock_alarm:
                called_callback = False
                buzzer_print_callback(publish_event, settings, status="OFF")
            current_clock_alarm = None
            

def is_after_current_time(date_str, time_str):
    from datetime import datetime
    target_datetime = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
    current_datetime = datetime.now().replace(second=0, microsecond=0)
    return current_datetime >= target_datetime