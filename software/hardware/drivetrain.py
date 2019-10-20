#!/usr/bin/env python3
import smbus
import math
import struct
import orientation
import numpy as np
import time

I2C_ADDRESS = 0x33

class DriveTrain:
    def __init__(self, bus=None, wheel_diameter=70.0, clicks_per_revolution=374):
        if bus is None:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = bus
        self.clicks_per_mm = clicks_per_revolution/(math.pi*wheel_diameter)
        self.orientation = orientation.MPU9250(bus=self.bus)
        results = []
        for i in range(20):
            results += [self.orientation.get_rotation()]
            time.sleep(0.02)
        self.gyro_cal = np.mean(results, axis=0)
        
    def mm2c(self, *args):
        return [int(x * self.clicks_per_mm) for x in args]
    
    def c2mm(self, *args):
        return [int(x / self.clicks_per_mm) for x in args]
                
    def stop(self):
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, [0])
            
    def drive(self, left, right):
        args = self.mm2c(left, right)
        command = struct.pack("<Bhh",1, *args)        
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))
        
    def goto_absolute(self, left, right, max_speed):
        args = self.mm2c(left, right, max_speed)
        command = struct.pack("<Biih", 2, *args)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))

    def individual(self, fr, fl, rr, rl):
        args = self.mm2c(fr, fl, rr, rl)
        command = struct.pack("<Bhhhh",4, *args)       
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x0, list(command))
                    
    def get_positions(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x10, 0x10)
        positions = struct.unpack("4i", bytes(data))
        return self.c2mm(*positions)

    def reset_position(self):
        data = struct.pack("<4i", 0, 0, 0, 0)
        self.bus.write_i2c_block_data(I2C_ADDRESS, 0x10, list(data))
        
    def goto(self, distance, max_speed):
        fr, fl, rr, rl = self.get_positions()
        right = (fr + rr) / 2
        left = (fl + rl) / 2
        self.goto_absolute(right+distance, left+distance, max_speed)
        
    def get_velocities(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x20, 0x08)
        velocities = struct.unpack("4h", bytes(data))
        return self.c2mm(*velocities)

    def get_constants(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x30, 0x10)
        p,i,d,ratio = struct.unpack("4f", bytes(data))
        return {'kP':p, 'kI':i, 'kD':d, 'ratio':ratio}

    def get_currents(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x40, 0x08)
        currents = struct.unpack("4h", bytes(data))
        return [x/1000 for x in currents]
    
    def get_voltages(self):
        data = self.bus.read_i2c_block_data(I2C_ADDRESS, 0x50, 0x08)
        peripheral, _, main, _ = struct.unpack("4h", bytes(data))
        peripheral /= 1000.0
        main /= 1000.0
        return (peripheral, main)
    
if __name__ == "__main__":
    import time
    driver = DriveTrain()
    driver.drive(400,-400)
    last_time = time.time()
    angle = 0
    print("CAL:", driver.gyro_cal)
    for i in range(5000):
        time.sleep(0.007)
        this_time = time.time()
        rotation = driver.orientation.get_rotation()-driver.gyro_cal
        rotation = rotation[2]*(this_time-last_time)
        angle += rotation
        print(rotation, angle, this_time-last_time)
        last_time = this_time
        if angle >=320.0:
            driver.drive(100,-100)
        if angle >=360.0:
            break;
    driver.stop()
    time.sleep(0.5)
    driver.stop()
    exit()
    time.sleep(0.01)
    print(driver.get_positions())
    driver.reset_position()
    print(driver.get_positions())
    time.sleep(0.01)
    driver.stop()
    time.sleep(1)
    driver.goto(1000,500)
    time.sleep(6)
    print(driver.get_positions())
    driver.goto(-1000,500)
    time.sleep(3)
    print(driver.get_positions())
    driver.stop()
