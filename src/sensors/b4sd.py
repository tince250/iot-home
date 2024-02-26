import RPi.GPIO as GPIO
import time
from locks import print_lock

class B4SD(object):
    def __init__(self, digits, segments, b4sd_queue, alarm_on_event, alarm_off_event,):
        self.digits = digits
        self.segments = segments
        self.num = {' ':(0,0,0,0,0,0,0),
            '0':(1,1,1,1,1,1,0),
            '1':(0,1,1,0,0,0,0),
            '2':(1,1,0,1,1,0,1),
            '3':(1,1,1,1,0,0,1),
            '4':(0,1,1,0,0,1,1),
            '5':(1,0,1,1,0,1,1),
            '6':(1,0,1,1,1,1,1),
            '7':(1,1,1,0,0,0,0),
            '8':(1,1,1,1,1,1,1),
            '9':(1,1,1,1,0,1,1)}
        self.b4sd_queue = b4sd_queue
        self.alarm_on_event = alarm_on_event
        self.alarm_off_event = alarm_off_event
        GPIO.setmode(GPIO.BCM)

        for digit in self.digits:
            GPIO.setup(digit, GPIO.OUT)
            GPIO.output(digit, 1)
        for segment in self.segments:
            GPIO.setup(segment, GPIO.OUT)
            GPIO.output(segment, 0)

    def show_time(self, current_alarm):
        if self.alarm_off_event.is_set() and current_alarm:
            current_alarm = None
            self.alarm_on_event.clear()
        try: 
            alarm = self.b4sd_queue.get(timeout=1)
            current_alarm = alarm
        except: 
            pass

        n = time.ctime()[11:13]+time.ctime()[14:16]
        s = str(n).rjust(4)

        for digit in range(4):
            for loop in range(0,7):
                GPIO.output(self.segments[loop], self.num[s[digit]][loop])
                if (int(time.ctime()[18:19])%2 == 0) and (digit == 1):
                    GPIO.output(25, 1)
                else:
                    GPIO.output(25, 0)
            GPIO.output(self.digits[digit], 0)
            time.sleep(0.001)
            GPIO.output(self.digits[digit], 1)

        if current_alarm and is_after_current_time(current_alarm['date'], current_alarm['time']):
            if not self.alarm_on_event.is_set():
                self.alarm_on_event.set()
            for digit in range(4):
                GPIO.output(self.digits[digit], 0)
            time.sleep(0.5)
            
        return str(n[:2])+":"+str(n[2:]), current_alarm

def run_b4sd_loop(b4sd, callback, stop_event, settings):
    current_alarm = None
    while True:
        current_time, current_alarm = b4sd.show_time(current_alarm)
        callback(settings, current_time)
        if stop_event.is_set():
            GPIO.cleanup()
            break

def is_after_current_time(date_str, time_str):
    from datetime import datetime
    target_datetime = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
    current_datetime = datetime.now().replace(second=0, microsecond=0)
    return current_datetime >= target_datetime