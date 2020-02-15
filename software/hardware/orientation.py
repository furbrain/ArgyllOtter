#!/usr/bin/env python3
import smbus
import struct
import math
import logging
import time
import numpy as np
from util import logged

MPU9250_ADDRESS = 0x68

class Orientation:
    def __init__(self, bus = None, address = MPU9250_ADDRESS):
        if bus is None:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = bus
        self.address = address
        self.bus.write_byte_data(self.address,27,0x10) #gyro 1000dps full scale
        self.bus.write_byte_data(self.address,28,0x08) #accel 4g full scale
        self.bus.write_byte_data(self.address,28,0x04) #accel 8ms low pass filter
        self.last_time = time.time()
        self.total_rotation = 0.0
        self.gyro_cal = [0,0,0]
    
        
    @logged
    def get_accel(self):
        data = self.bus.read_i2c_block_data(self.address, 0x3B, 0x06)
        accels = struct.unpack(">3h", bytes(data))
        return [(x*4.0/0x8000) for x in accels]
        
    @logged
    def get_angle(self, axis=2):
        accels = self.get_accel()
        distance = math.sqrt(sum(x*x for x in accels) - accels[axis]*accels[axis])
        angle = math.atan2(accels[axis],distance)
        angle  *= 180.0/math.pi 
        return angle
        
    def get_rotation(self):
        data = self.bus.read_i2c_block_data(self.address, 0x43, 0x06)
        rots = struct.unpack(">3h", bytes(data))
        return [(x*1000/0x8000) for x in rots]
        
    def calibrate_gyro(self):
        results = []
        for i in range(20):
            results += [self.get_rotation()]
            time.sleep(0.02)
        self.gyro_cal = np.mean(results, axis=0)

        
    def start_rotation(self):
        self.last_time = time.time()
        self.total_rotation = 0
        
    def get_total_rotation(self):
        this_time = time.time()
        rotation = self.get_rotation()-self.gyro_cal
        rotation = rotation[2]*(this_time-self.last_time)
        self.total_rotation += rotation
        self.last_time = this_time
        return self.total_rotation

        
if __name__ == "__main__":
    import time
    p = MPU9250(address=0x69)
    for x in range(100):
         time.sleep(0.5)
         print(p.get_angle())
