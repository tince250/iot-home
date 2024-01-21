#!/usr/bin/env python3
import MPU6050 
import time
import os

class Gyroscope(object):
    def __init__(self) -> None:
        self.mpu = MPU6050.MPU6050()     #instantiate a MPU6050 class object
        self.accel = [0]*3               #store accelerometer data
        self.gyro = [0]*3                #store gyroscope data
    
    def setup(self):
        self.mpu.dmp_initialize()    #initialize MPU6050
    
def run_gyro_loop(gyro, delay, callback, stop_event, publish_event, settings):
    while(True):
        accel = gyro.mpu.get_acceleration()      #get accelerometer data
        rotation = gyro.mpu.get_rotation()           #get gyroscope data
        
        angle = {
            "rotation_x": round(rotation[0] / 131.0, 2),
            "rotation_y": round(rotation[1] / 131.0, 2),
            "rotation_z": round(rotation[2] / 131.0, 2)
        }

        callback(angle, publish_event, settings)

        if stop_event.is_set():
            GPIO.cleanup()
            break
        time.sleep(delay)  # Delay between readings
        

