#!/usr/bin/env python3

from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime

class LCD(object):
    def __init__(self, **kwargs) -> None:
        self.PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        self.PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.

        try:
            self.mcp = PCF8574_GPIO(self.PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(self.PCF8574A_address)
            except:
                print ('I2C Address Error !')
                exit(1)
    
        self.lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=self.mcp)

    def get_cpu_temp(self):     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
        tmp = open('/sys/class/thermal/thermal_zone0/temp')
        cpu = tmp.read()
        tmp.close()
        return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
    
    def get_time_now(self):     # get system time
        return datetime.now().strftime('    %H:%M:%S')
        
    def show_text(self, text):
        self.mcp.output(3,1)     # turn on LCD backlight
        self.lcd.begin(16,2)     # set number of LCD lines and columns
        
        self.lcd.setCursor(0,0)  # set cursor position
        self.lcd.message( 'CPU: ' + self.get_cpu_temp()+'\n' )# display CPU temperature
        self.lcd.message( self.get_time_now() )   # display the time
        
        sleep(2)
        self.lcd.clear()
        
    def destroy(self):
        self.lcd.clear()

def run_lcd_loop(lcd, delay, callback, stop_event, settings, publish_event):
    print("tu sam")
    # while True:
    #     pressed_key = ms.get_pressed_key()
    #     if pressed_key:
    #         print(pressed_key)
    #         callback(pressed_key, settings, publish_event, True)
    #     if stop_event.is_set():
    #         lcd.destroy()
    #         GPIO.cleanup()
    #         break
    #     time.sleep(delay)
